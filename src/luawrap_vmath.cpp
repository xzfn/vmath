#define SOL_ALL_SAFETIES_ON 1
#include <sol/sol.hpp>

#include "luawrap_vmath.h"

#include <string>

#include "glm_util.h"

#include <glm/vec2.hpp>
#include <glm/vec3.hpp>
#include <glm/gtc/quaternion.hpp>
#include <glm/gtx/string_cast.hpp>


// sol::overload is more clear. but check_swap_arg_type reports better error message.
template<typename TLeft, typename TRight>
bool check_swap_arg_type(sol::object& left, sol::object& right, TLeft& out_left, TRight& out_right) {
	if (left.is<TLeft>() && right.is<TRight>()) {
		out_left = left.as<TLeft>();
		out_right = right.as<TRight>();
		return true;
	}
	if (left.is<TRight>() && right.is<TLeft>()) {
		out_left = right.as<TLeft>();
		out_right = left.as<TRight>();
		return true;
	}
	std::stringstream ss;
	ss << "wrong type: " << "expects ";
	ss << typeid(TLeft).name() << " and " << typeid(TRight).name();
	ss << ", got ";
	std::string left_type_name = sol::associated_type_name(left.lua_state(), 1, left.get_type());
	std::string right_type_name = sol::associated_type_name(right.lua_state(), 2, right.get_type());
	ss << left_type_name << " and " << right_type_name;
	throw std::invalid_argument(ss.str());
	return false;
}

namespace sol {
	template <>
	struct is_automagical<glm::vec3> : std::false_type {};
}

static void luawrap_Vector3(sol::table& m) {
	auto t = m.new_usertype<glm::vec3>("Vector3");

	auto vec3_new_default = []() {
		return glm::vec3(0.0f, 0.0f, 0.0f);
	};
	auto vec3_new = [](float x, float y, float z) {
		return glm::vec3(x, y, z);
	};
	t.set_function("new", sol::factories(vec3_new_default, vec3_new));

	t["x"] = &glm::vec3::x;
	t["y"] = &glm::vec3::y;
	t["z"] = &glm::vec3::z;

	t.set_function("length", [](glm::vec3& self) {
		return glm::length(self);
	});
	t.set_function("length_squared", [](glm::vec3& self) {
		return self.x * self.x + self.y * self.y + self.z * self.z;
	});
	t.set_function("dot", [](glm::vec3& self, glm::vec3& other) {
		return glm::dot(self, other);
	});
	t.set_function("cross", [](glm::vec3& self, glm::vec3& other) {
		return glm::cross(self, other);
	});
	t.set_function("normalize_self", [](glm::vec3& self) {
		self = glm::normalize(self);
	});
	t.set_function("normalize", [](glm::vec3& self) {
		glm::vec3 res = glm::normalize(self);
		return res;
	});

	t.set_function(sol::meta_function::equal_to, [](glm::vec3& self, glm::vec3& other) {
		return self == other;
	});
	t.set_function(sol::meta_function::addition, [](glm::vec3& self, glm::vec3& other) {
		return self + other;
	});
	t.set_function(sol::meta_function::multiplication, sol::overload(
		[](glm::vec3& self, float n) {
			return self * n;
		},
		[](float n, glm::vec3& self) {
			return self * n;
		}
	));
	t.set_function(sol::meta_function::subtraction, [](glm::vec3& self, glm::vec3& other) {
		return self - other;
	});
	t.set_function(sol::meta_function::unary_minus, [](glm::vec3& self) {
		return -self;
	});

	t.set_function("copy", [](glm::vec3 self) {
		return self;
	});
	t.set_function(sol::meta_function::to_string, [](glm::vec3& self) {
		return glm::to_string(self);
	});
}

namespace sol {
	template <>
	struct is_automagical<glm::quat> : std::false_type {};
}

static void luawrap_Quaternion(sol::table& m) {
	auto t = m.new_usertype<glm::quat>("Quaternion");

	auto quat_new_default = []() {
		return glm::quat(1.0f, 0.0f, 0.0f, 0.0f);
	};
	auto quat_new = [](float w, float x, float y, float z) {
		return glm::quat(w, x, y, z);
	};
	t.set_function("new", sol::factories(quat_new_default, quat_new));

	t["w"] = &glm::quat::w;
	t["x"] = &glm::quat::x;
	t["y"] = &glm::quat::y;
	t["z"] = &glm::quat::z;

	t.set_function("length", [](glm::quat& self) {
		return glm::length(self);
	});
	t.set_function("length_squared", [](glm::quat& self) {
		return self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z;
	});

	t.set_function("normalize_self", [](glm::quat& self) {
		self = glm::normalize(self);
	});
	t.set_function("normalize", [](glm::quat& self) {
		return glm::normalize(self);
	});

	t.set_function("slerp", [](glm::quat& self, glm::quat& other, float alpha) {
		return glm::slerp(self, other, alpha);
	});
	t.set_function("conjugate", [](glm::quat& self) {
		return glm::conjugate(self);
	});
	t.set_function("inverse", [](glm::quat& self) {
		return glm::inverse(self);
	});
	t.set_function("angle_axis", [](glm::quat& self) {
		float angle = glm::angle(self);
		glm::vec3 axis = glm::axis(self);
		return std::make_pair(angle, axis);
	});
	t.set_function("transform_point", [](glm::quat& self, glm::vec3 point) {
		return quat_transform_point(self, point);
	});
	t.set_function("transform_vector", [](glm::quat& self, glm::vec3 vector) {
		return quat_transform_vector(self, vector);
	});
	t.set_function("to_matrix3", [](glm::quat& self) {
		glm::mat3 matrix3 = glm::mat3_cast(self);
		return std::vector<glm::vec3>{ matrix3[0], matrix3[1], matrix3[2] };
	});
	t.set_function("to_matrix4", [](glm::quat& self) {
		return glm::mat4_cast(self);
	});
	t.set_function("from_angle_axis", sol::factories([](float angle, glm::vec3 axis) {
		return glm::angleAxis(angle, axis);
	}));
	t.set_function("from_matrix3", sol::factories([](std::vector<glm::vec3>& matrix3) {
		glm::mat3 matrix3_(matrix3[0], matrix3[1], matrix3[2]);
		return glm::quat_cast(matrix3_);
	}));
	t.set_function("euler_angles", &quat_to_euler_angles);
	t.set_function("from_euler_angles", sol::factories(euler_angles_to_quat));
	t.set_function("from_from_to_rotation", sol::factories(from_to_rotation_to_quat));
	t.set_function("from_look_rotation", sol::factories(look_rotation_to_quat));

	t.set_function(sol::meta_function::multiplication, [](glm::quat& self, glm::quat& other) {
		return self * other;
	});

	t.set_function("copy", [](glm::quat self) {
		return self;
	});

	t.set_function(sol::meta_function::to_string, [](glm::quat& self) {
		return glm::to_string(self);
	});
}


namespace sol {
	template <>
	struct is_automagical<glm::mat4> : std::false_type {};
}

static void luawrap_Matrix4(sol::table& m_) {
	auto t = m_.new_usertype<glm::mat4>("Matrix4");

	auto mat4_new_default = []() {
		return glm::mat4(1.0f);
	};
	auto mat4_new = [](
		float m00, float m01, float m02, float m03,
		float m10, float m11, float m12, float m13,
		float m20, float m21, float m22, float m23,
		float m30, float m31, float m32, float m33) {
		return glm::mat4(
			m00, m01, m02, m03,
			m10, m11, m12, m13,
			m20, m21, m22, m23,
			m30, m31, m32, m33
		);
	};
	t.set_function("new", sol::factories(mat4_new_default, mat4_new));

	t["m00"] = sol::property(
		[](glm::mat4& m) { return m[0][0]; },
		[](glm::mat4& m, float f) { m[0][0] = f; });
	t["m01"] = sol::property(
		[](glm::mat4& m) { return m[0][1]; },
		[](glm::mat4& m, float f) { m[0][1] = f; });
	t["m02"] = sol::property(
		[](glm::mat4& m) { return m[0][2]; },
		[](glm::mat4& m, float f) { m[0][2] = f; });
	t["m03"] = sol::property(
		[](glm::mat4& m) { return m[0][3]; },
		[](glm::mat4& m, float f) { m[0][3] = f; });

	t["m10"] = sol::property(
		[](glm::mat4& m) { return m[1][0]; },
		[](glm::mat4& m, float f) { m[1][0] = f; });
	t["m11"] = sol::property(
		[](glm::mat4& m) { return m[1][1]; },
		[](glm::mat4& m, float f) { m[1][1] = f; });
	t["m12"] = sol::property(
		[](glm::mat4& m) { return m[1][2]; },
		[](glm::mat4& m, float f) { m[1][2] = f; });
	t["m13"] = sol::property(
		[](glm::mat4& m) { return m[1][3]; },
		[](glm::mat4& m, float f) { m[1][3] = f; });

	t["m20"] = sol::property(
		[](glm::mat4& m) { return m[2][0]; },
		[](glm::mat4& m, float f) { m[2][0] = f; });
	t["m21"] = sol::property(
		[](glm::mat4& m) { return m[2][1]; },
		[](glm::mat4& m, float f) { m[2][1] = f; });
	t["m22"] = sol::property(
		[](glm::mat4& m) { return m[2][2]; },
		[](glm::mat4& m, float f) { m[2][2] = f; });
	t["m23"] = sol::property(
		[](glm::mat4& m) { return m[2][3]; },
		[](glm::mat4& m, float f) { m[2][3] = f; });

	t["m30"] = sol::property(
		[](glm::mat4& m) { return m[3][0]; },
		[](glm::mat4& m, float f) { m[3][0] = f; });
	t["m31"] = sol::property(
		[](glm::mat4& m) { return m[3][1]; },
		[](glm::mat4& m, float f) { m[3][1] = f; });
	t["m32"] = sol::property(
		[](glm::mat4& m) { return m[3][2]; },
		[](glm::mat4& m, float f) { m[3][2] = f; });
	t["m33"] = sol::property(
		[](glm::mat4& m) { return m[3][3]; },
		[](glm::mat4& m, float f) { m[3][3] = f; });

	t.set_function("transform_point", [](glm::mat4& self, glm::vec3 point) {
		return transform_point(self, point);
	});
	t.set_function("transform_vector", [](glm::mat4& self, glm::vec3 vector) {
		return transform_vector(self, vector);
	});
	t.set_function("project_point", [](glm::mat4& self, glm::vec3 point) {
		return project_point(self, point);
	});
	t.set_function("inverse", [](glm::mat4& self) {
		return glm::inverse(self);
	});
	t.set_function("transpose", [](glm::mat4& self) {
		return glm::transpose(self);
	});
	t.set_function("to_transform", [](glm::mat4& self) {
		return mat4_to_transform(self);
	});
	t.set_function(sol::meta_function::multiplication, [](glm::mat4& self, glm::mat4& other) {
		return self * other;
	});
	t.set_function(sol::meta_function::addition, [](glm::mat4& self, glm::mat4& other) {
		return self + other;
	});
	t.set_function(sol::meta_function::subtraction, [](glm::mat4& self, glm::mat4& other) {
		return self - other;
	});
	t.set_function("mul_scalar", [](glm::mat4& self, float s) {
		return self * s;
	});

	t.set_function("from_orthographic", sol::factories([](float left, float right, float bottom, float top, float z_near, float z_far) {
		return glm::ortho(left, right, bottom, top, z_near, z_far);
	}));
	t.set_function("from_perspective", sol::factories([](float fov, float aspect, float z_near, float z_far) {
		return glm::perspective(fov, aspect, z_near, z_far);
	}));

	t.set_function("copy", [](glm::mat4 self) {
		return self;
	});

	t.set_function(sol::meta_function::to_string, [](glm::mat4& self) {
		return glm::to_string(self);
	});
}


namespace sol {
	template <>
	struct is_automagical<Transform> : std::false_type {};
}

static void luawrap_Transform(sol::table& m) {
	auto t = m.new_usertype<Transform>("Transform");

	auto transform_new_default = []() {
		return Transform();
	};
	auto transform_new = [](glm::vec3 translation, glm::quat rotation, glm::vec3 scale) {
		return Transform(translation, rotation, scale);
	};
	t.set_function("new", sol::factories(transform_new_default, transform_new));

	t["translation"] = &Transform::translation;
	t["rotation"] = &Transform::rotation;
	t["scale"] = &Transform::scale;

	t.set_function("transform_point", [](Transform& self, glm::vec3 point) {
		return transform_point(self, point);
	});
	t.set_function("transform_vector", [](Transform& self, glm::vec3 vector) {
		return transform_vector(self, vector);
	});
	t.set_function("inverse", [](Transform& self) {
		return transform_inverse(self);
	});
	t.set_function("to_matrix4", [](Transform& self) {
		return transform_to_mat4(self);
	});

	t.set_function(sol::meta_function::multiplication, [](Transform& self, Transform& other) {
		return self * other;
	});

	t.set_function("copy", [](Transform self) {
		return self;
	});
	t.set_function(sol::meta_function::to_string, [](Transform& self) {
		return to_string(self);
	});
}


namespace sol {
	template <>
	struct is_automagical<glm::vec2> : std::false_type {};
}

static void luawrap_Vector2(sol::table& m) {
	auto t = m.new_usertype<glm::vec2>("Vector2");

	auto vec2_new_default = []() {
		return glm::vec2(0.0f, 0.0f);
	};
	auto vec2_new = [](float x, float y) {
		return glm::vec2(x, y);
	};
	t.set_function("new", sol::factories(vec2_new_default, vec2_new));

	t["x"] = &glm::vec2::x;
	t["y"] = &glm::vec2::y;

	t.set_function("length", [](glm::vec2& self) {
		return glm::length(self);
	});
	t.set_function("length_squared", [](glm::vec2& self) {
		return self.x * self.x + self.y * self.y;
	});
	t.set_function("dot", [](glm::vec2& self, glm::vec2& other) {
		return glm::dot(self, other);
	});
	t.set_function("normalize_self", [](glm::vec2& self) {
		self = glm::normalize(self);
	});
	t.set_function("normalize", [](glm::vec2& self) {
		glm::vec2 res = glm::normalize(self);
		return res;
	});

	t.set_function(sol::meta_function::equal_to, [](glm::vec2& self, glm::vec2& other) {
		return self == other;
	});
	t.set_function(sol::meta_function::addition, [](glm::vec2& self, glm::vec2& other) {
		return self + other;
	});
	t.set_function(sol::meta_function::multiplication, sol::overload(
		[](glm::vec2& self, float n) {
			return self * n;
		},
		[](float n, glm::vec2& self) {
			return self * n;
		}
	));
	t.set_function(sol::meta_function::subtraction, [](glm::vec2& self, glm::vec2& other) {
		return self - other;
	});
	t.set_function(sol::meta_function::unary_minus, [](glm::vec2& self) {
		return -self;
	});

	t.set_function("copy", [](glm::vec2 self) {
		return self;
	});
	t.set_function(sol::meta_function::to_string, [](glm::vec2& self) {
		return glm::to_string(self);
	});
}


namespace sol {
	template <>
	struct is_automagical<glm::vec4> : std::false_type {};
}

static void luawrap_Vector4(sol::table& m) {
	auto t = m.new_usertype<glm::vec4>("Vector4");

	auto vec4_new_default = []() {
		return glm::vec4(0.0f, 0.0f, 0.0f, 0.0f);
	};
	auto vec4_new = [](float x, float y, float z, float w) {
		return glm::vec4(x, y, z, w);
	};
	t.set_function("new", sol::factories(vec4_new_default, vec4_new));

	t["x"] = &glm::vec4::x;
	t["y"] = &glm::vec4::y;
	t["z"] = &glm::vec4::z;
	t["w"] = &glm::vec4::w;

	t.set_function("length", [](glm::vec4& self) {
		return glm::length(self);
	});
	t.set_function("length_squared", [](glm::vec4& self) {
		return self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w;
	});
	t.set_function("dot", [](glm::vec4& self, glm::vec4& other) {
		return glm::dot(self, other);
	});
	t.set_function("normalize_self", [](glm::vec4& self) {
		self = glm::normalize(self);
	});
	t.set_function("normalize", [](glm::vec4& self) {
		glm::vec4 res = glm::normalize(self);
		return res;
	});

	t.set_function(sol::meta_function::equal_to, [](glm::vec4& self, glm::vec4& other) {
		return self == other;
	});
	t.set_function(sol::meta_function::addition, [](glm::vec4& self, glm::vec4& other) {
		return self + other;
	});
	t.set_function(sol::meta_function::multiplication, [](sol::object left, sol::object right) {
		glm::vec4 self;
		float n;
		check_swap_arg_type<glm::vec4, float>(left, right, self, n);
		return self * n;
	});
	t.set_function(sol::meta_function::subtraction, [](glm::vec4& self, glm::vec4& other) {
		return self - other;
	});
	t.set_function(sol::meta_function::unary_minus, [](glm::vec4& self) {
		return -self;
	});

	t.set_function("copy", [](glm::vec4 self) {
		return self;
	});
	t.set_function(sol::meta_function::to_string, [](glm::vec4& self) {
		return glm::to_string(self);
	});
}


namespace sol {
	template <>
	struct is_automagical<Ray> : std::false_type {};
}

static void luawrap_Ray(sol::table& m) {
	auto t = m.new_usertype<Ray>("Ray");

	auto ray_new_default = []() {
		return Ray();
	};
	auto ray_new = [](glm::vec3 position, glm::vec3 direction) {
		return Ray(position, direction);
	};
	t.set_function("new", sol::factories(ray_new_default, ray_new));

	t["position"] = &Ray::position;
	t["direction"] = &Ray::direction;

	t.set_function("copy", [](Ray self) {
		return self;
	});
	t.set_function(sol::meta_function::to_string, [](Ray& self) {
		return "Ray(" + glm::to_string(self.position) + ", " + glm::to_string(self.direction) + ")";
	});
}

static void luawrap_vmath(sol::table& m) {
	luawrap_Vector3(m);
	luawrap_Quaternion(m);
	luawrap_Matrix4(m);
	luawrap_Transform(m);
	luawrap_Vector2(m);
	luawrap_Vector4(m);
	luawrap_Ray(m);
}

int luaopen_vmath(lua_State* L) {
	sol::state_view lua(L);
	sol::table m = lua.create_table();
	luawrap_vmath(m);
	sol::stack::push(lua, m);
	return 1;
}
