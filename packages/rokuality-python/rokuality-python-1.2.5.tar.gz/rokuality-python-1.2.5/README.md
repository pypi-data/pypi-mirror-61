# Rokuality Python - End to End Automation for Roku, XBox, Playstation, Cable SetTop Boxes, and More!

The Rokuality platform allows you to distribute Roku, XBox, PS4, and Cable SetTop Box end to end tests across multiple devices on your network. The project goal is to provide a no cost/low cost open source solution for various video streaming platforms that otherwise don't offer an easily automatable solution! Clone and start the [Rokuality Server](https://github.com/rokuality/rokuality-server), and start writing tests!

### Your Roku tests in the cloud!

Access the [Rokuality Device Cloud](https://www.rokuality.com/) to run your Roku tests in a CI/CD fashion from anywhere in the world! Get access to all the popular Roku streaming devices for both automated and live device test sessions on the world's first Roku Webdriver device cloud. Your [device portal](https://www.rokuality.com/device-portal-and-site-services) will allow you to review your test history, manage your test teams, review run results, and more! Our [detailed documentation](https://www.rokuality.com/roku-automation) will get you and your team up and running quickly. Start a [free trial](https://www.rokuality.com/plans-pricing) today and get started!

### Getting started: Get the Server
Clone/Download and start the [Rokuality Server](https://github.com/rokuality/rokuality-server) which acts as a lightweight web server proxy for your test traffic. The server does all the 'heavy lifting' on the backend.

### Getting started: Add the bindings to your Project
To use Rokuality in your tests or application, install the `rokuality-python` dependency:
```xml
    pip install rokuality-python
```

### Getting started: Roku
See the [Getting Started: Roku](https://github.com/rokuality/rokuality-server) section for details about preparing your Roku device for test. The Rokuality framework is one of the first projects to provide support for the [Roku WebDriver API](https://github.com/rokudev/automated-channel-testing).

### Getting started: XBox
See the [Getting Started: XBox](https://github.com/rokuality/rokuality-server) section for details about preparing your XBox device for test.

### Getting started: HDMI Connected Devices (Playstation, Cable SetTopBox, AndroidTV, AppleTV, and More)
See the [Getting Started: HDMI Connected Devices (Playstation, Cable SetTopBox, AndroidTV, AppleTV, and More](https://github.com/rokuality/rokuality-server) section for details about preparing your Cable Settop Box, Playstation, AndroidTV, or AppleTV device for test.

### The Basics:
The Rokuality bindings operate via Image Based Object Recognition and OCR techniques to identify 'elements' on the device screen and return them to your test scripts as Objects for verification and interaction. The project is modeled after the Selenium/Appium structure so if you've used those toolsets for browsers/mobile devices previously - this framework will look and feel very comfortable to you. See the [Roku example tests](https://github.com/rokuality/rokuality-python/blob/master/tests/test_roku.py) or [XBox example tests](https://github.com/rokuality/rokuality-python/blob/master/tests/test_xbox.py) or [HDMI example tests](https://github.com/rokuality/rokuality-python/blob/master/tests/test_playstation.py) for a full list of samples.

#### Declare a driver to connect to the server:
```python
    '''Roku'''
    driver = RokuDriver("http://yourserverurl:yourrunningserverport", self.capabilities)

    '''XBox'''
    driver = XBoxDriver("http://yourserverurl:yourrunningserverport", self.capabilities)

    '''HDMI device (playstation, cable settop box, androidtv, appletv, etc)'''
    driver = HDMIDriver("http://yourserverurl:yourrunningserverport", self.capabilities)
```
This will take care of installing/launching your device app package (if Roku or XBox), ensure the device is available and ready for test, and start a dedicated session on your device as indicated via your DeviceCapabilities object. See [Device Capabilities](#device-capabilities-explained) for an explanation of what capabilities are available for your driver startup.

#### Finding elements:
There are two primary ways of finding elements on your device that are available for all device types:

1) TEXT
```python
    driver.finder().find_element(By().text("text to find on screen"))
```
In this example, the Rokuality server will capture the image from your device screen, and then perform an evaluation against the found text within that image and match it against your locator. If your locator text is NOT found, then a NoSuchElementException will be thrown. Tesseract is the default OCR engine used to perform textual evaluations. But you can optionally indicate that you want to use GoogleVision's OCR engine which requires you have a valid VisionUI service account setup with Google. See [Using Google Vision](#using-google-vision-ocr) for those details. But for most use cases, using the default tesseract engine is enough.

2) IMAGE - local image snippet file
```python
    driver.finder().find_element(By().image("/path/to/your/image/snippet.png"))
```
In this example, you can provide the path to an image snippet that you expect to be contained within your device screen. The server will then ship this image snippet to itself, capture the device screen, and evaluate if it exists on the device.

OR

3) IMAGE - url to to an image snippet file
```python
    driver.finder().find_element(By().image("http://urltoyourimagesnippet.png"))
```
In this example, you can provide a url to your locator image snippet and the server will download that image and evaluate it against the device screen. Useful for those more dynamic testing situations where you may want to query your application feeds to get the dynamic app images for evaluation, or if you want to keep your image based locators in a remote repository.

#### Finding elements with Roku WebDriver:
Optionally when testing on Roku you can provide the following native based locator types:
```oython
    element_by_text = roku_driver.finder().find_element(RokuBy().text('text to search for'))
    element_by_tag = roku_driver.finder().find_element(RokuBy().tag('tag'))
    element_by_attribute = roku_driver.finder().find_element(RokuBy().attribute('attribute', 'attribute value'))
```

#### Finding multi match elements:
You can search for multiple element matches from a singular locator and return the results of match to an Element collection as follows:
```python
    elements = driver.finder().find_elements(By().text("locator that will return multiple matches"))
```
When using `find_elements`, a NoSuchElementException will NOT be thrown to the user in the event that an element is not found. In that event the collection will be empty. So this method can be used to determine if an element is present or not:

```python
    elements = driver.finder().find_elements(By().text("locator"))
    if (len(elements) == 0):
            print("element is not present")
```

#### Elements as objects:
A found element can be stored to an object and additional details about it can be retrieved:
```python
    element = self.roku_driver.finder().find_element(By().text("Hello World!"))
    print("element x: " + str(element.get_x()))
    print("element y: " + str(element.get_y()))
    print("element width: " + str(element.get_width()))
    print("element height: " + str(element.get_height()))
    print("element confidence: " + str(element.get_confidence()))
    print("element text: " + element.get_text())
```
The element details include the elements location and size details as found on the device, the text contained within the match (relevent if an image snippet locator was provided), and the confidence score of the match with higher values indicating the confidence in your find:
```xml
    368
    319
    45
    19
    91.33713
    Hello World!
```

#### Sending remote control commands to the device - Roku and XBox:
To send remote button presses to the device you can do the following:
```python
    '''roku'''
    driver.remote().press_button(RokuButton.SELECT)
    
    '''xbox'''
    driver.remote().press_button(XBoxButton.A)
```
All remote commands are available. See [roku remote command](https://github.com/rokuality/rokuality-python/blob/master/src/enums/roku_button.py) or [xbox remote command](https://github.com/rokuality/rokuality-python/blob/master/src/enums/xbox_button.py) for all available remote buttons. Also you can send literal characters to the device if you need to interact with a Roku or XBox search selector (Note the virtual keyboard must be visible on the screen at the time this call is made):
```python
    driver.remote().send_keys("typing out hello world on a search screen")
```

Note that by default, the time delay between multiple remote control commands is 0 milliseconds, meaning multiple remote control commands will happen as quickly as possible. This can in some cases lead to test flake due to multiple commands happening back to back too quickly. If this is happening, you can add a delay in between remote control button presses as follows:
```python
    """
    sets a delay between remote control button presses to 2 seconds. this will last for the duration of the session or until a new value is set. If not set, defualts to 0
    """
    driver.options().set_remote_interact_delay(2000)
```

#### Sending remote control commands to the device - HDMI Devices (Playstation, Cable SetTop, AndroidTV, AppleTV, and more):
To send remote button presses to the HDMI/IR device you can do the following:
```java
    '''get a list of available remote commands for your device'''
    button_options = driver.remote().get_button_options()
    print(button_options)
    
    '''send the desired button press to the device'''
    driver.remote().press_button("DirectionUp")
    driver.remote().press_button("Guide")
    driver.remote().press_button("Select")
```

#### Getting screen artifacts:
Various methods exist for getting screen artifacts such as the screen image, sub screen image, screen recording during test, and screen text:

```python
    '''get screen size'''
    driver.screen().get_screen_size()

    '''get screen image'''
    driver.screen().get_image()

    '''get the screen sub image from starting x,y with width/height'''
    driver.screen().get_image_sub_screen(1, 1, 300, 300)

    """get the screen recording of the test session from start to now
       note that the screen recordings are created by stitching the collected device screenshots
       together and video quality won't be the best"""
    driver.screen().get_recording()

    '''get the xml page source of the channel. useful for debugging Roku Webdriver locators'''
    xml_source = driver.screen().get_page_source()
```

#### Getting screen text:
Screen text of the device is returned as a collection of ScreenText objects as found on the screen. Each ScreenText item will be an object containing details about the found device text such as location, height, and width of the word as found on the device screen:
```python
    screen_texts = roku_driver.screen().get_text()
    for screen_text in screen_texts:
        x = screen_text.get_x()
        y = screen_text.get_y()
        width = screen_text.get_width()
        height = screen_text.get_height()
        confidence = screen_text.get_confidence()
```

Alternatively you can get the entire device screen as a full string via `driver.screen().get_text_as_string()`

#### Getting information about the media player (ROKU ONLY):
For Roku devices, it's possible to get details about your media player in flight through the Roku WebDriver rest api which can be accessed in your test code as follows:
```python
    '''gets information about the media in flight including state, bitrate, encoding information, and much much more!'''
    media_player_info = self.roku_driver.info().get_media_player_info()
    assert media_player_info.is_error() == False
    assert media_player_info.is_live() == False
    assert media_player_info.get_state() == 'none'
```

#### Getting performance data from your application during test (ROKU ONLY):
Roku provides a way to measure your app's cpu and memory utilization through their brightscript profiler. Our platform allows you to access the brightscript performance profile during the course of your test. To utilize this functionality you must provide the 'EnablePerformanceProfiling' capability on test session start and set the value to true. This will take your provided sideloadable .zip package, update the manifest with the necessary values for profile capturing, and then recompile for automation on your device.

```python
    self.capabilities.add_capability('EnablePerformanceProfiling', True)
    self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)

    performance_profile = self.roku_driver.info().get_performance_profile()
    performance_profile_mb = os.path.getsize(performance_profile) / 1000000
    print("Performance profile MB size: " + str(performance_profile_mb))
```

Once you've retrieved your .bsprof file during test - this file can be uploaded to [Roku's profiler visualization tool](http://devtools.web.roku.com/profiler/viewer/) to see the performance data in a friendly user format.

#### Getting debug log info (ROKU ONLY):
For Roku devices, it's possible to get the debug logs as follows:
```python
    log_content = self.driver.info().get_debug_logs()
```

#### Device Capabilities explained:
Various capabilities and values can be provided and passed to your driver instance at startup. Some of them are required and others are optional. The following are the minimum capabilities **required** to start a driver session.

#### Roku
```python
    '''init a capability object'''
    capabilities = DeviceCapabilities()

    '''indicates you want a Roku test'''
    capabilities.add_capability("Platform", "Roku")

    '''set the path or url to your sideloadable .zip'''
    capabilities.add_capability("AppPackage", "path/or/url/to/your/apppackage")

    '''set your roku ip address'''
    capabilities.add_capability("DeviceIPAddress", "yourdeviceipaddress")

    '''set your device username and password'''
    capabilities.add_capability("DeviceUsername", "yourdeviceusername")
    capabilities.add_capability("DevicePassword", "yourdevicepassword")

    '''set your OCR module - options are "Tesseract" or "GoogleVision"'''
    capabilities.add_capability("OCRType", "Tesseract")
    
    '''pass the capabilities and start your driver'''
    driver = RokuDriver("http://yourserverurl:yourrunningserverport", capabilities)
```

#### Xbox
```python
    '''init a capability object'''
    capabilities = DeviceCapabilities()

    '''indicates you want a XBox test'''
    capabilities.add_capability("Platform", "XBox")

    '''set the path or url to your .appxbundle package to install'''
    capabilities.add_capability("AppPackage", "path/or/url/to/your/apppackage")

    '''the app id - will be the friendly app name of your appxbundle'''
    capabilities.add_capability("App", "appid")

    '''set your xbox ip address'''
    capabilities.add_capability("DeviceIPAddress", "yourdeviceipaddress")

    '''set your console xbox live username and password for the logged in user'''
    capabilities.add_capability("DeviceUsername", "your_xbox_live_username")
    capabilities.add_capability("DevicePassword", "your_xbox_live_password")

    """
    set your xbox live console id
    can be found from your xbox dev settings page at https://your_xbox_device_ip:11443/#Settings
    """
    capabilities.add_capability("DeviceID", "your_xbox_live_console_id")

    '''set your OCR module - options are "Tesseract" or "GoogleVision"'''
    capabilities.add_capability("OCRType", "Tesseract")
    
    '''pass the capabilities and start your driver'''
    driver = XBoxDriver("http://yourserverurl:yourrunningserverport", capabilities)
```

#### HDMI Devices (Playstation, Cable SetTop, AndroidTV, AppleTV, and more)
```python
    '''init a capability object'''
    capabilities = DeviceCapabilities()

    '''indicates you want an HDMI test'''
    capabilities.add_capability("Platform", "HDMI")

    '''set your logitech harmony info. see the why harmony and harmony setups section of the main server page for details'''
    capabilities.add_capability("HomeHubIPAddress", "yourharmonyipaddress")
    capabilities.add_capability("DeviceName", "devicenameassavedinharmony")

    """the video input and audio input names of your attached hdmi capture card. They can be found by running
    the following commands:
    MAC: ~/Rokuality/dependencies/ffmpeg_v4.1 -f avfoundation -list_devices true -i ""
    WINDOWS: ~\Rokuality\dependencies\ffmpeg_win_v4.1\bin\ffmpeg.exe -list_devices true -f dshow -i dummy
    """
    capabilities.add_capability("VideoCaptureInput", "video input name")
    capabilities.add_capability("AudioCaptureInput", "audio input name")

    '''set your OCR module - options are "Tesseract" or "GoogleVision"'''
    capabilities.add_capability("OCRType", "Tesseract")
    
    '''pass the capabilities and start your driver'''
    driver = HDMIDriver("http://yourserverurl:yourrunningserverport", capabilities)
```

| Capability  | Description | Required Or Optional | Notes |
| ------------- | ------------- | ------------- | ------------- |
| Platform | Indicates the target platform for the tests.  | Required | String - Options are 'Roku, 'XBox', or 'HDMI' |
| AppPackage | The sideloadable zip to be installed (Roku), or the .appxbundle (XBox). Must be a valid file path OR a valid url.  | Required for Roku and XBox - IF the 'App' capability is not provided. Ignored for HDMI devices | String |
| App | The friendly id of your app for Roku and XBox. For Roku this cap is optional. If you provide this cap and ommit the 'AppPackage' cap then the device will attempt to launch an already installed channel - Note that this can be an installed production channel id which you can retrieve from your device via `curl http://yourdeviceip:8060/query/apps`. But if you launch a production Roku channel you MUST have a connected HDMI capture card and provide the requisite `VideoCaptureInput` and `AudioCaptureInput` capabilities. For XBox this cap is always required and MUST be the app id of your installed .appxbundle - if you ommit the 'AppPackage' cap then the device will attempt to launch an already installed appxbundle matching this id. |Roku = Optional. XBox = Required. HDMI = Ignored | String |
| DeviceIPAddress | The ip address of your Roku or XBox. Ignored for HDMI.  | Required for Roku or XBox | String - Your device MUST be reachable from the machine running the Rokuality server. |
| DeviceUsername | Roku = The dev console username created when you enabled developer mode on your device. XBox = The XBox live username signed into the XBox console.  | Required - Roku and XBox | String |
| DevicePassword | Roku = The dev console password created when you enabled developer mode on your device. XBox = The XBox live password signed into the XBox console.   | Required - Roku and XBox | String |
| DeviceID | XBox - the XBox live console id. Ignored for Roku and HDMI.   | Required - XBox | String |
| ImageMatchSimilarity | An optional image match similarity default used during Image locator evaluations. A lower value will allow for greater tolerance of image disimilarities between the image locator and the screen, BUT will also increase the possibility of a false positive.  | Optional | Double. Defaults to .90 |
| ScreenSizeOverride | An optional 'WIDTHxHEIGHT' cap that all screen image captures will be resized to prior to match evaluation. Useful if you want to enforce test consistence across multiple device types and multiple developer machines or ci environments.  | Optional | String - I.e. a value of '1800x1200' will ensure that all image captures are resized to those specs before the locator evaluation happens no matter what the actual device screen size is.  |
| OCRType | The OCR type - Options are 'Tesseract' OR 'GoogleVision'. In most cases Tesseract is more than enough but if you find that your textual evalutions are lacking reliability you can provide 'GoogleVision' as a more powerful alternative. BUT if the capability is set to 'GoogleVision' you MUST have a valid Google Vision account setup and provide the 'GoogleCredentials' capability with a valid file path to the oath2 .json file with valid credentials for the Google Vision service.  | Required | String 
| GoogleCredentials | The path to a valid .json Google Auth key service file. | Optional but Required if the 'OCRType' capability is set to 'GoogleVision' | The .json service key must exist on the machine triggering the tests. See [Using Google Vision](#using-google-vision-ocr) for additional details.  |
| HomeHubIPAddress | The ip address of your logitech harmony hub. | Required for HDMI. Ignored for Roku and XBox | String - See the [why harmony](https://github.com/rokuality/rokuality-server) and [configuring your harmony](https://github.com/rokuality/rokuality-server) sections of the server page for details. |
| DeviceName | The name of your device as saved in your Harmony hub i.e. 'MyPlaystation4'. | Required for HDMI. Ignored for Roku and XBox | String |
| VideoCaptureInput | The name of your video card capture video input if running an HDMI connected test. Will vary by the type of hdmi capture card. | Required for HDMI device types (Playstation, Cable SetTop Box, AndroidTV, AppleTV, etc. Optional for Roku if you wish to test a production channel. Ignored for XBox | Can be found by running a terminal command. For MAC: `~/Rokuality/dependencies/ffmpeg_v4.1 -f avfoundation -list_devices true -i ""` and for Windows: `~\Rokuality\dependencies\ffmpeg_win_v4.1\bin\ffmpeg.exe -list_devices true -f dshow -i dummy` |
| AudioCaptureInput | The name of your video card capture audio input if running an HDMI connected test. Will vary by the type of hdmi capture card. | Required for HDMI device types (Playstation, Cable SetTop Box, AndroidTV, AppleTV, etc. Optional for Roku if you wish to test a production channel. Ignored for XBox | Can be found by running a terminal command. For MAC: `~/Rokuality/dependencies/ffmpeg_v4.1 -f avfoundation -list_devices true -i ""` and for Windows: `~\Rokuality\dependencies\ffmpeg_win_v4.1\bin\ffmpeg.exe -list_devices true -f dshow -i dummy` |
| MirrorScreen | If provided with a widthxheight value, then a window will be launched on the user's desktop showing the test activity in real time for the duration of the test session. Useful for debugging tests on remote devices.  | Optional | String - 'widthxheight' format. i.e. '1200x800' will launch a screen mirror with width 1200, and height 800. |
| EnablePerformanceProfiling | Roku only. If provided your sideloadable .zip package will be updated for performance profiling. Then during the course of the execution you can retrieve the .bsprof file with CPU and memory utilization data from your channel.  | Optional | Boolean - true to allow for performance capturing. Defaults to false. |

#### Element Timeouts and Polling:
There are two main options when it comes to element timeouts and polling

Timeouts - By default the element timeout is set to 0 milliseconds, meaning if the driver fails to find an element immediately, it will throw a NoSuchElement exception. But a better practice is to set a implicit wait timeout so the driver will poll for a duration, trying to find the element before it fails and throws the NoSuchElementException:

```python
    '''will fail immediately'''
    driver.finder().find_element(By().text("no such text"))
```
vs
```python
    '''will fail after 5 seconds'''
    driver.options().set_element_timeout(5000)
    driver.finder().find_element(By().text("no such text"))
```
It is generally recommended to set respective timeouts to reduce test flake, but setting the values too high can increase test duration.

Additionally you can set the interval of how often the element search polling will happen. In this example, the same timeout is applied but the element polling will happen every second. If the polling interval is ommited the default is 250 milliseconds.
```python
    '''will fail after 5 seconds polling every second'''
    driver.options().set_element_timeout(5000)
    driver.options().set_element_poll_interval(1000)
    driver.finder().find_element(By().text("no such text"))
```

#### Using Google Vision OCR:
As mentioned previously, Tesseract is the default OCR engine used when you provide a text based locator. And the Rokuality server ships the relevant trained data files so the more you use it during test, the better it will get at finding the provided text based locators. But if you find that's not as reliable as needed for your testing purposes you can use Google Vision as an alternative provided you have a valid [Google Vision](https://cloud.google.com/vision/docs/before-you-begin) account setup. You must also set the path to your .json service file containing your service key in your DeviceCapabilities prior to driver start.

```python
    capabilities = DeviceCapabilities()
    capabilities.add_capability("OCRType", "GoogleVision")
    capabilities.add_capability("GoogleCredentials", "/path/to/your/vision/authkey.json")
```

#### Failing to find elements? :
Image Based Locators `By().image("pathorurltoyoourimagesnippet.png")`
1. Make sure your locator image snippet is in a valid image format. Most tests use .png format so for best results please use locators of this type.
2. Make sure that your image snippets are in good quality and you are doing an apples to apples comparison of the image snippet you wish to find within the screen image. Some image snipping tools are better than others, so if capturing static image snippets for later locator use be wary of the tools you're using. Alternatively, you can get a subscreen section from the device during test and save it as a static locator for later use.
`locator_to_use_later = driver.screen().get_image_sub_screen(40, 80, 160, 220)`
3. You can optionally set the "ImageMatchSimilarity" DeviceCapability at driver startup which will set a tolerance for image comparisons. Lower values will mean a greater likelihood of getting a match, but too low of a value will introduce a false positive.
`capabilities.add_capability("ImageMatchSimilarity", .85)`

Text Based Locators `By().text("text to search for")`
1. Check that your string isn't too complicated, i.e. a locator of `By().text("hello world")` is much more likely to be found than a locator of `By().text("he!!O W@rLd!#!")`. Also, single world locators are better than multiple world locators but we continue to work on the server back end to improve the reliability.
2. As mentioned previously, Tesseract is the default OCR engine but if you're finding that the results aren't as reliable as you'd like, consider using [Google Vision](#using-google-vision-ocr) as an alternative.
3. You can access the entire decoded device screen text by `driver.screen().get_text_as_string()`. If your locator is present in the string but not found during test, please log a bug on the [issues](https://github.com/rokuality/rokuality-java/issues) page and we'll investigate.
4. By default the OCR evaluations happen against the entire device screen but sometimes it's better to narrow the scope of the find to a smaller region of the screen to get better results. This can be done with `driver.finder().find_element_sub_screen(by, 100, 500, 300, 200)` which will limit the scope of the find to that subset of the screen and likely return better results.

#### Server timeouts and orphaned sessions:
At the end of every driver session, you should close the driver and cleanup all session data by calling the stop method:
```python
    '''stop the driver and clean up all resources'''
    driver.stop()
```
But if you don't a safety exists to eventually clean up those assets. The server session will listen for new commands and will timeout if no commands for the session have been received for a specified duration. The default command timeout is set to 60 seconds - meaning if a session is started and no commands are sent to it for 60 seconds, then the session will automatically be terminated and released. You can increase/decrease this time by setting the 'commandtimeout' option when you launch the server. See the [Server Command Options](https://github.com/rokuality/rokuality-server) section of the server for details.