#pragma once

#include <lua.hpp>

#ifdef vmath_EXPORTS
#define vmath_API __declspec(dllexport)
#else
#define vmath_API
#endif

extern "C" vmath_API int luaopen_vmath(lua_State * L);
