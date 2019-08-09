##自动化脚本规则 

###1、文件目录规则
   1、API目录下按照服务名称进行文件夹命名（如web-order、casecenter），各服务下按照接口调用方类型命名文件夹（h5、pc、app），
  如接口调用方无区别可以忽略，具体可参考git已有结构
  
   2、testcase下目录分为流程（flowcase）、单接口（singlecase）、抽取的模块（modulecase）三个子目录
   
   3、testsuites下可不建立子目录
###2、脚本命名规则
   1、api 脚本以接口名称最后部分作为名称，不含格式（jtml）
   
   2、testcase 模块脚本以包含的接口拼接作为名称以’_‘连接，顺序与内部调用顺序一致（不建议包含过多接口），单接口以接口名称加场景命名（例如cancelCase_parameter_abnormal）
   流程脚本以业务场景命名
###3、脚本编写规则
   1、 API接口,接口中需要测试的重点字段需要参数化，非必要字段、系统无特殊处理字段、修改频率低的字段不需要参数化，
   参数化字段尽量在API接口脚本中以variables形式定义默认值，调用时只需要传入需要的字段变量即可
   
   2、testcase中两个及以上接口结合使用多次，需要抽取成自定义模块，以减少脚本重复增加复用
   
   3、与环境相关数据需参数化（如数据库、域名，用户名，密码等等），使用配置文件.env
   
   4、脚本需要添加必要注释：API接口需注明API名称、定义参数的含义（可选）、参数的枚举值，自定义模块类需注明模块流程名称
   流程类脚本需要注明各case的场景名称，debugtalk中需注明各函数的意义
###4、代码提交   
   1、脚本提交git：调试通过的脚本及时提交git，提交时需要去除本地生成的编译信息（idea文件、pyc文件、生成的测试报告）
   2、提交时需注明修改内容（add or modify or del）
   
   
   