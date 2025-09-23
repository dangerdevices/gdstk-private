include(GNUInstallDirs)

find_package(Python COMPONENTS Interpreter Development.Module NumPy REQUIRED)

python_add_library(_gdstk MODULE WITH_SOABI "gdstk_module.cpp")

target_compile_features(_gdstk PRIVATE cxx_std_11)

target_link_libraries(_gdstk PRIVATE gdstk Python::NumPy)

# Statically link libstdc++ on Linux.
#
# On machines with Cadence installed, the system libstdc++ may be a
# newer version than the Cadence-provided one. CDBA _must_ dynamically
# link to the Cadence libstdc++, which causes conflicts.
#
# Gdstk's use of C++ is strictly internal, so it can use its own
# libstdc++ and not have to care what anyone else does.
if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    target_link_options(_gdstk PRIVATE -static-libgcc -static-libstdc++)
endif()

install(TARGETS _gdstk
    COMPONENT _gdstk
    DESTINATION ${SKBUILD_PROJECT_NAME})

