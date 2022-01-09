cmake_minimum_required(VERSION 3.19)

# build lua vmath extension

project(luavmath)

set(CMAKE_CXX_STANDARD 17)

find_package(Lua REQUIRED)
find_package(sol2)
find_package(glm)

set(vmath_SOURCES
	src/glm_util.h
	src/glm_util.cpp
	src/luawrap_vmath.h
	src/luawrap_vmath.cpp
)

add_library(vmath SHARED ${vmath_SOURCES})
target_include_directories(vmath PUBLIC ${LUA_INCLUDE_DIR})
if (MSVC)
	target_compile_options(vmath PRIVATE "/bigobj")
endif ()
target_link_libraries(vmath PRIVATE sol2 glm::glm ${LUA_LIBRARY})
