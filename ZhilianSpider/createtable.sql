create table source_zhilian(
     zwmc varchar(50),
     fkl varchar(50),
     gsmc varchar(50),
     zwyx varchar(50),
     gzdd varchar(50),
     zwmcurl varchar(100),
     fl varchar(200),
     gzjy varchar(50),
     zdxl varchar(50),
     zprs varchar(50),
     zwms varchar(500),
     cjsj datetime,
     source varchar(30),
     level varchar(10)
 )DEFAULT CHARSET=utf8;



create  table source_zhilian_errlog(
     msg varchar(500),
     err varchar(500),
     sj datetime
 )DEFAULT CHARSET=utf8;