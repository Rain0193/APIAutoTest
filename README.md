# 1 简介

    接口自动化测试框架。
    1. 支持Json协议业主端、员工端、物业后台、运营后台、商家后台接口快速调用。
    2. 解决签名、token、AES及3DES加解密等问题，可解析APP入参及后端出参。
    3. 测试数据与执行脚本分离。
    4. 支持数据库操作，初始化、销毁测试数据。
    5. pytest组织管理用例及测试数据。
    6. 日志跟踪存储、控制台打印、方便调试。
	
	需要掌握的知识点：
	1. python基本语法。重点：字典、列表、条件判断。
	2. yaml的字典、列表、多层嵌套的写法。参考模板就可以。
	
	以上两点基本可以进行接口测试，若要进行接口自动化，需要掌握以下：
	1. SQL的基本增删改查写法。
	2. pytest的fixture及对应的scope。

# 2 安装、配置

1. Python3.4以上
2. Requests 
3. pycrypto  注意：若是Python3.5以上，装加密库时设置变量%VS100COMNTOOLS%有点不一样，请度娘。
4. pytest
5. yaml
6. pymysql
7. pytest-html


# 3 目录文件说明

    APITest：根目录
        config：配置目录
        testdata：yaml格式的测试数据目录
        testcase：测试脚本目录
        util：工具类目录
		log：日志目录
		report：报告目录
		.gitignore：git push时要忽略的文件
		CHANGELOG.md：版本记录文件
		README.md：项目说明文件
		requirements.txt：依赖库说明文件
		
> 注意：Pycharm记得设置成UTF-8编码
    
# 4 开发Tips

## 4.1 data模板

**注意冒号的前后需要空格！**

    
    --- # 测试数据文档开始
    # 接口名称
    name : 3.1 新增收货地址
    api_name : user/addReceiveAddress
    project_name : user
    setup : update mimidb.t_mm_user_receive_address set is_delete=1 where user_id=1884251359479808   #在数据库表前面必须加上数据库信息。若是test_suite级别的setup、teardown则放在最外面的那层。
    case1 :
        case_name : test_add_normal_address  #对应着testcase的名字
        setup :  # test_case级别的setup、teardown若需要则加上。
        teardown :  # test_case级别的setup、teardown若需要则加上。
        params :  #根据接口文档的入参填写
            model :
                provinceId : 27730
                cityId : 27731
                areaId : 27793
                streetId : 27806
                address : 黄埔大道西78号恒大中心
                consignee : 自动化测试收货人
                mobile : 13688888888
        verify1 : 自动化测试收货人 #若有多个校验点，在字段后加数据标识，使用时对应改变。
        verify2 : 13688888888
        verify3 : verify_sql : SELECT address_id from mimidb.t_mm_user_receive_address where is_delete=0 and user_id=1884251359479808 ORDER BY address_id desc limit 1 ;
    

### 4.1.1 字典嵌套列表

    
    type :
        - 1  #英文横线，前后有空格
        - 2
    
    对应 { "type" : [1,2] } type的值是一个列表
        
### 4.1.2 列表嵌套字典

    - name : TavisD
    - age : 18
    对应 [ { "name" : "TavisD" }, { "age" : 18 } ]
    
    


## 4.2 testcase模板

### 4.2.1 文件头

每个testcase都一样

    
    import os
    import sys
    import pytest
    
    sys.path.append( os.path.dirname( os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ) ) )
    from utils.api_client import APIClient
    from utils.file_util import FileUtil
    from utils.mysql_util import MysqlUtil
    from utils.gen_util import GenUtil
    
    api_client = APIClient( )  # 接口核心类实例
    file_util = FileUtil( )  # 文件类实例
    mysql_util = MysqlUtil( )  # 操作数据库类实例
    gen_util = GenUtil( )  # 生成测试数据类实例
    test_data, yml_file_path = file_util.get_test_data_by_name( os.path.abspath( __file__ ) )  # 获取测试数据、测试数据的文件名
    url = api_client.cal_url( test_data[ "project_name" ], test_data[ "api_name" ] )  # 生成接口URL
    

    
    ######------------------------以上，每个py文件都一样。----------------------######
    



### 4.2.2 普通接口测试

    
    def test_add_normal_address( ):  # 对应的测试数据的名字与它一样
        '''
        使用正常数据添加收货地址
        :return:
        '''
        params = test_data[ "case1" ][ "params" ]  # 入参
        result = api_client.http_post( url, params, api_client.NORMAL_TOKEN )  # 发送请求，并拿到返回值
        assert result[ "result" ][ "consignee" ] == test_data[ "case1" ][ "verify1" ]  # 断言校验点1，一般接口测试可以通过肉眼判断结果，加断言的目的更多于自动化
        assert result[ "result" ][ "mobile" ] == test_data[ "case1" ][ "verify2" ]  # 断言校验点2
    


### 4.2.3 使用动态数据进行测试

    
    def test_add_normal_address( ):  # 对应的测试数据的名字与它一样
        '''
        使用正常数据添加收货地址
        :return:
        '''
        # 当我们使用动态生成测试数据时：
        # 1.把入参及对应的校验点改成动态生成的数据。
        # 2.为了跟踪测试时用了什么测试数据，所以把测试数据保存下。
        test_data[ "case1" ][ "verify1" ] = test_data[ "case1" ][ "params" ][ "model" ][
            "consignee" ] = gen_util.gen_chinese_name( )
        test_data[ "case1" ][ "params" ][ "model" ][ "mobile" ] = test_data[ "case1" ][ "verify2" ] = gen_util.gen_phones( )
        file_util.save_test_data_by_name( yml_file_path, test_data )
    
        params = test_data[ "case1" ][ "params" ]  # 入参
        result = api_client.http_post( url, params, api_client.NORMAL_TOKEN )  # 发送请求，并拿到返回值
        assert result[ "result" ][ "consignee" ] == test_data[ "case1" ][ "verify1" ]  # 断言校验点1
        assert result[ "result" ][ "mobile" ] == test_data[ "case1" ][ "verify2" ]  # 断言校验点2
    

### 4.2.4 使用skip跳过用例

有些用例在接口测试时要测试，但设计成自动化意义不大，可通过``@pytest.mark.skip``跳过

    
    @pytest.mark.skip  # 若自动化时，觉得不需要该用例，可以跳过
    def test_add_address_using_special_symbol( ):
        '''
        使用特殊符号、空格添加收货地址
        :return:
        '''
        params = test_data[ "case2" ][ "params" ]
        result = api_client.http_post( url, params, api_client.NORMAL_TOKEN )
        assert result[ "result" ] != None
    

### 4.2.4 使用自带的setup teardown方式进行初始化及销毁数据

使用该方式时，testcase不需要增加参数，方便很多

    
    def setup_module( module ):  # module表示scope是module
        mysql_util.update( test_data[ "suite_setup" ] )
        print( "setuping module" )
    
    
    def tear_down( module ):  # module表示scope是module
        print( "tearing module" )
        
    def test_add_normal_address(  ):  # 对应的测试数据的名字与它一样
        '''
        使用正常数据添加收货地址
        :return:
        '''
        params = test_data[ "case1" ][ "params" ]  # 入参
        result = api_client.http_post( url, params, api_client.NORMAL_TOKEN )  # 发送请求，并拿到返回值
        assert result[ "result" ][ "consignee" ] == test_data[ "case1" ][ "verify1" ]  # 断言校验
        assert result[ "result" ][ "mobile" ] == test_data[ "case1" ][ "verify2" ]  # 断言校验
    

### 4.2.5 使用fixture进行初始化及销毁数据

fixture不仅可以做这种简单场景的工作，还可以组合、传递参数做更复杂的工作

    
    # pytest V2.9版本及V3.X以上都支持，由于allure报告目前只支持到pytest V2.9版本，暂时采用这种兼容方式写法
    @pytest.fixture( scope = "module" )  # 添加一个fixture，作用范围是module
    def setup_and_teardown( request ):  # request，固定写法
        # setup的事情
        print( "setup module" )
    
        # teardown的事情，封装在一个方法里
        def teardown( ):
            print( "teardown module" )
    
        # 把teardown添加请求的最后，做清理工作，固定写法
        request.addfinalizer( teardown )
    
    
    # pytest V3.0以上版本官方推荐该方式
    @pytest.fixture( scope = "module" )
    def setup_and_teardown( request ):
        print( "setup module" )
    
        yield
    
        print( "teardown module" )
    
    def test_add_normal_address( setup_and_teardown ):  # 哪个测试用例要用到初始化销毁，就把上面定义的初始化销毁方法的名称扔过来
        '''
        使用正常数据添加收货地址
        :return:
        '''
        params = test_data[ "case1" ][ "params" ]  # 入参
        result = api_client.http_post( url, params, api_client.NORMAL_TOKEN )  # 发送请求，并拿到返回值
        assert result[ "result" ][ "consignee" ] == test_data[ "case1" ][ "verify1" ]  # 断言校验
        assert result[ "result" ][ "mobile" ] == test_data[ "case1" ][ "verify2" ]  # 断言校验	
        
    
### 4.2.6 登录Token类型及加密说明

    http_post(url, params, token, login_type = LOGIN_TYPE_NORMAL, crypto_type = "3DES")方法默认是登录业主端“LOGIN_TYPE_NORMAL”，加密默认是IOS使用的3DES
    1. 因为根据token无法判断出哪种类型的token，所以若使用运营平台、物业后台、商家后台等非业主端时，需要加上“login_type”参数，否则接口会出现“请先登录”提示。如：``api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )``
    2. 若需要使用安卓，需要加上“crypto_type”参数，值为“AES”
    3. 使用自己的测试账号。如``api_client.NORMAL_TOKEN_XXX``  #业主端，XXX的账号

## 4.3 项目代码管理说明

    1. 在Git项目建自己的分支，以dev + 自己的名字拼音为分支名（如dev-dengxihong），代码来源于master。master是主开发分支，开发者没有合并权限。
    2. 用source tree克隆代码时，在高级选项输入自己的分支名（如dev-dengxihong）。
    3. 每次提交（commit）代码到本地仓库时，先拉取master分支的代码。若拉取下来的代码跟自己的有冲突（软件会有提示或代码里会有<<<<<字样），需要解决冲突后，再推送（push）到自己的开发分支（如dev-dengxihong）。
    4. 推送到自己的分支后，在Merge Request --> New Merge Request -->源分支选择自己的分支（如dev-dengxihong），目标分支选master --> 填写合并简要 --> master的owner同意合并即完成代码合并。

    
# 6. Bugs



[更新记录](CHANGELOG.md)