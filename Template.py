log4j_quite = """
log4j.rootLogger=fatal, stdout
log4j.appender.stdout=org.apache.log4j.ConsoleAppender
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern=%%5p [%%t] (%%F:%%L) - %%m%%n
"""

log4j_file = """
log4j.rootLogger=debug, R

log4j.appender.stdout=org.apache.log4j.ConsoleAppender
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern=%%5p [%%t] (%%F:%%L) - %%m%%n

log4j.appender.R=org.apache.log4j.RollingFileAppender
log4j.appender.R.File=%(FILE_NAME)s

log4j.appender.R.MaxFileSize=100KB
log4j.appender.R.layout=org.apache.log4j.PatternLayout
log4j.appender.R.layout.ConversionPattern=%%p %%t %%c - %%m%%n
"""

log4j2_file = """
status = warn
dest = err
name = PropertiesConfig
 
property.filename = %(FILE_NAME)s.2
 
appender.file.type = File
appender.file.name = MyFILE
appender.file.fileName = ${filename}
appender.file.layout.type = PatternLayout
appender.file.layout.pattern = %%d %%p %%C{1.} [%%t] %%m%%n
 
rootLogger.level = DEBUG
rootLogger.appenderRef.file.ref = MyFILE
"""
