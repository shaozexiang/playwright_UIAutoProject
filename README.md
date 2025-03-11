## 框架介绍

主要使用到的技术为python + playwright + allure + log + mysql + Jenkins + paddle

## 实现功能

*   playwright定位元素，支持原生的语法规则，只需要学习playwright的原生语法即可实现功能
*   测试数据隔离, 实现数据驱动
*   支持多接口数据依赖: 如A接口需要同时依赖B、C接口的响应数据作为参数
*   数据库断言: 直接在测试用例中写入查询的sql即可断言，无需编写代码
*   动态多断言: 如接口需要同时校验响应数据和sql校验，支持多场景断言
*   统计接口的运行时长: 拓展功能，订制开关，可以决定是否需要使用
*   日志模块: 打印每个接口的日志信息，同样订制了开关，可以决定是否需要打印日志
*   钉钉、企业微信通知: 支持多种通知场景，执行成功之后，可选择发送钉钉、或者企业微信、邮箱通知
*   自定义拓展字段: 如用例中需要生成的随机数据，可直接调用

## 目录结构

```markdown
playwright_web_project
│ conftest.py // 全局conftest，提供全局配置信息诸如浏览器配置等
│ connect_browser.bat // 调试代码用的bat，可以手动启动或者通过命令行，需要手动更改chromium的名称为具体的版本
│ main.py // 启动入口
│ pytest.ini // pytest的配置信息
│ README.md // help
│
├─auto // cookies登录凭证存放的json位置
│ cookies.json
│      
├─config                                       
│ config.yaml // 全局配置文件
│      __init__.py
│      
├─data // 调用接口使用的用例数据
│              
├─file                                           
│ ├─api_upload_file // 接口上传文件路径
│ ├─api_export_file // 接口下载文件路径
│ ├─ui_export_file // UI下载文件路径
│ └─ui_upload_file // UI上传文件路径
│          
├─js_file // javascript代码路径
│ full_screen.js
│      
├─logs // 输出的日志文件
├─output // 输出的报告层面
│ ├─image // 输出的报告层面
│ │ ├─error_image // 图像验证失败的图片
│ │ ├─screen_image // UI层截图路径
│ │ └─verify_image // 验证的图片
│ └─report // allure报告
├─page // 页面层
│ │ common_page.py
│ │ page_factory.py
│ │  __init__.py
│ │  
│ ├─component // 组件层
│ │ │ button.py
│ │ │ div.py
│ │ │ img.py
│ │ │ input.py
│ │ │ liItem.py
│ │ │ span.py
│ │ │ table.py
│ │ │  __init__.py
│          
├─plugins                                        
│ │ pytest_playwright.py // playwright插件
│ │
│ │         
├─service // 服务层
│ │  __init__.py
│ │  
│ ├─route_management_service
│ ├─task_management_service
│          
├─test-result // 测试结果
├─test_case // 测试用例
│ │ conftest.py // testcase局部的conftest，提供热加载机制
│ │ debug_testcase.py // 单条用例执行debug
│ │  __init__.py
├─utils
│ │  __init__.py
│ │  
│ ├─allure_tools
│ │ │ allure_report_data.py // allure数据清理
│ │ │ allure_report_handler.py // allure报告处理
│ │ │ allure_step_handler.py // allure step封装
│ │ │ error_case_excel.py // 异常用例发送
│ │ │  __init__.py
│ │
│ │
│ ├─assertion
│ │ │ assert_control.py // 断言数据
│ │ │ assert_type.py // 接口的断言类型
│ │ │  __init__.py
│ │ │  
│ │
│ │          
│ ├─cache_process
│ │ │ cache_control.py // 缓存处理
│ │ │ redis_control.py // redis缓存处理
│ │ │  __init__.py
│ │ │
│ │
│ ├─database_tools
│ │ mysql_control.py // mysql数据库CRUD
│ │      __init__.py
│ │      
│ ├─locator_tools
│ │ │ base_page.py // 页面层基类，封装playwright基本操作
│ │ │ locator_decorator.py
│ │ │  __init__.py
│ │ │
│ │          
│ ├─logging_tools // 日志控制模块
│ │ │ log_control.py
│ │ │ log_decorator.py
│ │ │ run_time_decorator.py
│ │ │  __init__.py
│ │ │
│ │  
│ ├─notify_tools // 通知模块
│ │ │ ding_talk.py
│ │ │ lark.py
│ │ │ send_mail.py
│ │ │ wechat_send.py
│ │ │  __init__.py
│ │ │   
│ │
│ ├─other_tools
│ │ │ exceptions.py // 自定义异常
│ │ │ get_file_path.py // 获取实际的文件路径
│ │ │ get_local_ip.py // 获取ip地址
│ │ │ jsonpath_date_replace.py // 替换请求数据
│ │ │ locator_type_mapping.py // 定位类型映射
│ │ │ models.py // 自定义验证类型
│ │ │ thread_tool.py // 多线程
│ │ │  __init__.py
│ │ │  
│ │ ├─install_tool // pip下载失败的备用库
│ │ │ install_requirements.py
│ │ │ version_library_comparisons.txt
│ │ │      __init__.py
│ │ │
│ │
│ ├─process_tools // 进程线程处理模块
│ │ │ process_handler.py
│ │ │  __init__.py
│ │ │   
│ ├─read_files_tools // 读写文件模块
│ │ │ clean_files.py // 清除路径文件
│ │ │ excel_control.py // excel读写
│ │ │ get_yaml_data_analysis.py // yaml数据解析验证
│ │ │ regular_control.py // 正则匹配
│ │ │ yaml_control.py // 读写yaml文件
│ │ │  __init__.py
│ │ │
│ ├─requests_tools
│ │ │ dependent_case.py // 依赖控制
│ │ │ encryption_algorithm_control.py // 加密算法
│ │ │ request_control.py // 请求控制
│ │ │ set_current_request_cache.py // 请求过程中的缓存控制
│ │ │ teardown_control.py // 后置数据清理
│ │ │  __init__.py
│ │ │       
│ ├─time_tools
│ │ │ time_control.py // 时间相关方法
│ │ │  __init__.py

```

## 依赖库

```markdown
aiofiles==0.8.0
albucore==0.0.13
albumentations==1.4.10
allure-pytest==2.13.5
allure-python-commons==2.13.5
annotated-types==0.7.0
anyio==4.4.0
asgiref==3.5.1
astor==0.8.1
asttokens==2.4.1
async-timeout==4.0.3
atomicwrites==1.4.0
attrs==24.2.0
backcall==0.2.0
bcrypt==4.2.0
beautifulsoup4==4.12.3
bleach==6.1.0
blinker==1.4
Brotli==1.0.9
cachetools==5.5.0
certifi==2021.10.8
cffi==1.15.0
chardet==4.0.0
charset-normalizer==2.0.7
click==8.1.3
colorama==0.4.4
colorlog==6.6.0
contourpy==1.3.0
crypto==1.4.1
cryptography==36.0.0
cssselect==1.2.0
cssutils==2.11.1
cycler==0.12.1
Cython==3.0.11
decorator==5.1.1
defusedxml==0.7.1
DingtalkChatbot==1.5.3
docopt==0.6.2
et-xmlfile==1.1.0
eval_type_backport==0.2.0
exceptiongroup==1.2.2
execnet==1.9.0
executing==2.1.0
exif==1.6.0
Faker==9.8.3
fastjsonschema==2.20.0
fire==0.6.0
Flask==2.0.3
fonttools==4.53.1
greenlet==3.1.1
h11==0.13.0
h2==4.1.0
hpack==4.0.0
httpcore==1.0.5
httptools==0.4.0
httpx==0.27.2
hyperframe==6.0.1
idna==3.3
imageio==2.35.1
imgaug==0.4.0
importlib_metadata==8.4.0
importlib_resources==6.4.4
imutils==0.5.4
iniconfig==1.1.0
ipython==8.12.3
itchat==1.3.10
itsdangerous==2.1.2
jedi==0.19.1
Jinja2==3.1.2
joblib==1.4.2
jsonpath==0.82
jsonschema==4.23.0
jsonschema-specifications==2023.12.1
jupyter_client==8.6.2
jupyter_core==5.7.2
jupyterlab_pygments==0.3.0
kaitaistruct==0.9
kiwisolver==1.4.5
lazy_loader==0.4
ldap3==2.9.1
lmdb==1.5.1
loguru==0.7.2
lxml==5.3.0
MarkupSafe==2.1.1
matplotlib==3.9.2
matplotlib-inline==0.1.7
mistune==3.0.2
mitmproxy==8.1.1
more-itertools==10.5.0
msgpack==1.0.3
multidict==6.0.2
Naked==0.1.32
nbclient==0.10.0
nbconvert==7.16.4
nbformat==5.10.4
networkx==3.2.1
numpy==1.26.4
opencv-contrib-python==4.10.0.84
opencv-python==4.10.0.84
opencv-python-headless==4.10.0.84
openpyxl==3.0.9
opt-einsum==3.3.0
packaging==21.3
paddleocr==2.9.1
paddlepaddle==2.6.1
pandocfilters==1.5.1
paramiko==3.5.0
parso==0.8.4
passlib==1.7.4
pathvalidate==3.2.1
pickleshare==0.7.5
pillow==10.4.0
pipreqs==0.5.0
platformdirs==4.2.2
playwright==1.48.0
pluggy==1.5.0
plum-py==0.8.7
premailer==3.10.0
prompt_toolkit==3.0.47
protobuf==3.19.4
psutil==6.1.0
publicsuffix2==2.20191221
pure_eval==0.2.3
py==1.11.0
pyasn1==0.4.8
pyclipper==1.3.0.post5
pycparser==2.21
pydantic==2.10.0
pydantic_core==2.27.0
pyDes==2.0.1
pydivert==2.1.0
pyee==12.0.0
Pygments==2.18.0
PyMySQL==1.0.2
PyNaCl==1.5.0
pyOpenSSL==21.0.0
pyparsing==3.0.6
pyperclip==1.8.2
pypng==0.0.21
PyQRCode==1.2.1
pytest==8.3.3
pytest-base-url==2.1.0
pytest-dependency==0.6.0
pytest-forked==1.3.0
pytest-playwright==0.5.1
pytest-rerunfailures==14.0
pytest-xdist==2.4.0
python-dateutil==2.8.2
python-docx==1.1.2
python-slugify==8.0.4
pywin32==304
PyYAML==5.4.1
pyzmq==26.2.0
rapidfuzz==3.9.7
redis==4.3.6
referencing==0.35.1
requests==2.32.3
requests-toolbelt==0.9.1
rpds-py==0.20.0
ruamel.yaml==0.17.21
ruamel.yaml.clib==0.2.6
sanic==22.3.1
sanic-routing==22.3.0
scikit-image==0.24.0
scikit-learn==1.5.2
scipy==1.13.1
shapely==2.0.6
shellescape==3.8.1
six==1.16.0
sniffio==1.3.1
sortedcontainers==2.4.0
soupsieve==2.6
sshtunnel==0.4.0
stack-data==0.6.3
termcolor==2.4.0
text-unidecode==1.3
threadpoolctl==3.5.0
tifffile==2024.8.30
tinycss2==1.3.0
toml==0.10.2
tomli==2.0.1
tornado==6.4.1
tqdm==4.66.5
traitlets==5.14.3
typing_extensions==4.12.2
urllib3==1.26.7
urwid==2.1.2
wcwidth==0.2.13
webencodings==0.5.1
websockets==10.3
Werkzeug==2.1.2
win32-setctime==1.1.0
wsproto==1.1.0
xlrd==2.0.1
xlutils==2.0.0
xlwings==0.27.7
xlwt==1.3.0
yagmail==0.15.293
yarg==0.1.9
zipp==3.20.1
zstandard==0.17.0

```

## 使用介绍

**前序中会介绍自动化的分层和UI自动化的优劣势**

### 前序

#### 自动化测试的分层

自动化测试常见会被分成三个层次，分别为Unit(单元)、service(接口+集成)、web(UI测试或者称之为系统测试) 从收益的角度来说Unit>
service>web
单元测试往往是由开发完成，所以大部分测试人员只需要考虑service和web。
接口自动化相对于UI自动化来说不需要考虑界面的因素更加的简单，他只需要考虑接口之间的关系，也正因如此接口自动化没有办法模拟真实用户行为。

#### UI自动化测试的优势

1.  模拟用户的行为，根据用例模拟用户可能的操作更加贴近用户的实际行为
2.  依赖于浏览器，如果是存在一定的其他引擎的页面则有可能发现一些在手工测试中难以发现的页面加载问题
3.  解放一定的人力资源，一个完善的UI自动化可以减少测试人员一直重复执行相同的测试用例的情况，让测试人员可以有更多的时间去思考需求
4.  加快回归测试，在测试过程中发现问题越早越能够降低修复的成本，在推送代码之后通过UI自动化完成回归测试可以第一时间发现是否本次更新造成了旧有用例的执行失败

#### UI自动化测试的劣势

1.  依赖于页面元素，由于依赖于浏览器中的组件定位所以在开发更改前端组件代码之后会出现定位不到的情况
2.  维护成本高，由于上述的第一点原因，每次代码改动都可能导致用例执行失败
3.  运行时间长，一个复杂用例往往会有很多个定位元素和不同的页面进行交互，所以执行时间往往会很长
4.  投入产出难度量，测试随着用户界面的变化而变化。因此，UI 测试需要更长的时间，从而延迟交付。最终，很难估计持续运行 UI 测试的
    ROI。

### 如何使用

#### 结构介绍

这里分为三层的代码编写**page**、**service**、**testcase**，

*   page层： page层里面封装单个页面的所有操作，这里要保证单个page存放的只是单个页面的操作
    *   component层：component层封装基本的定位操作和定位元素的返回
    *   断言部分：断言可以继承于page层，因为断言部分大部分都是需要通过定位到page层的元素进行断言，所以二者使用的元素是可能相似的
*   service层：与实际业务直接挂钩，按照项目的业务编写即可
*   testcase层：
    1.  只需要存放测试用例即可，大部分逻辑都在service层已经实现了，更多是用例隔离和数据预处理、数据清理的工作。
    2.  当然也可以采用第二种思路在这里传入实际的上需要fill的值

相对于原始的PO(page object)模式，框架在po模式的基础上增加了新的component层，由于前端基本都是采用了组件化开发往往你看到的控件还会复用到同一个项目的不同处
这样封装的对象就可以从原始的单个元素变为控件元素。这样封装有什么用的好处呢？具体请看下面的例子

```markdown
<button>提交</button> #更改前的组件
<button><span>提交</span></button> #更改后的组件
```

更改前的定位方式 `locator('\\button')` 更改后的定位方式`locator('\\button\\span')`
，更改前和更改后只是增加了一层span元素，对于前端来说可能只是为了输出的文本更加优美。<br>
按照原先的PO模式，前端更改了组件库的代码会影响到你定位相同组件的代码，**又由于这些代码散落在你的page页面**
，你需要到每一个页面上去查看是否有使用到这个定位方式`locator('\\button')` 将他修改为新的定位方式。<br>
如果你使用的是新的结构，你只需要修改**component**层上的**button**文件内的对应的定位方式即可。

#### 如何编写测试用例

1.  编写component层，可以根据不同的组件类型进行分类比如button、div、span、img、table等，根据名称+组件类型进行元素定位
2.  page调用component层,完成本页面的元素定位和具体操作
3.  service层实例化page层对象，通过实例化对象调用元素操作完成单条测试用例的编写和断言处理
4.  testcase层组装service层和fixture完成一条用例从 **数据预处理->用例执行->数据清理** 整个过程

**具体请参考testcase里面提供的测试用例，那里有基础的测试用例**


\*\*warming：这里由于component是page的基类，所以一定需要保证component是封装的一个组件而非元素，在修改后确定修改对其他元素定位没影响
\*\* <br>

#### 相比原先的playwright增加了什么

1.  playwright本身已经提供了非常丰富的定位方式，所以只是在原先的定位方式上增了简单的图像验证和OCR识别以处理一些特殊的情况比如需要比较的是图像而不是数值
2.  增加了allure报告内输出playwright提供的trace、screen和video，在allure报告的`_artifact_recorder`
    后置处理中可以看到在当前用例执行时的视频和trace文件，在test\_body中会截图所有的操作在浏览器的位置
3.  异常信息输出，分开常见的定位元素不唯一和定位元素超时的情况

## 安装教程

首先，执行本框架之后，需要搭建好 python、jdk、 allure、playwright环境

```shell
pip install -r requirements.txt
```

**playwright下载对应的浏览器启动**

```shell
playwirght install 
```

