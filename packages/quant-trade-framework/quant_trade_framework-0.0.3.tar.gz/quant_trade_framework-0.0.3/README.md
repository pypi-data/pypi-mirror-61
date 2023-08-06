# GeneralQuantTradeClient
通用量化交易框架客户端，用户获取平台数据

#20191129创建初始版本

#20191130增加bar数据获取接口
(1)初始化数据库连接配置,以下是标准配置，直接使用源代码，配置文件在conf目录下
database_manager = initialize.init(setting.SETTINGS)
(2) database_manager.load_bar_data 获取bar数据接口，包含五个参数
symbol: str 合约名称，比如"M9999.XDCE"
exchange: str,交易所，默认使用"test""
interval: str,bar数据聚合时间，目前只有"1m"
start: datetime, 查询开始时间，时间格式符合"2019-11-07 09:00:00"这种格式
end: datetime, 查询结束时间，时间格式符合"2019-11-07 09:00:00"这种格式
数据接口返回panda.dataframe对象