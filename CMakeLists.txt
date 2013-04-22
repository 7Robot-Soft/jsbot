cmake_minimum_required(VERSION 2.6.0)

project(Js C)

#set_source_files_properties(jsread.c PROPERTIES COMPILE_FLAGS "-std=gnu99")

add_library(jsread SHARED jsread.c)
install(TARGETS jsread LIBRARY DESTINATION lib)
