include(GNUInstallDirs)

find_package(Python COMPONENTS Interpreter Development.Module NumPy REQUIRED)

python_add_library(_gdstk MODULE WITH_SOABI "gdstk_module.cpp")

target_compile_features(_gdstk PRIVATE cxx_std_11)

target_link_libraries(_gdstk PRIVATE gdstk Python::NumPy)

# On machines with Cadence installed, use the libstd++ it provides,
# rather than the system-wide one.
#
# This prevents version conflicts when the Cadence libstdc++ version
# differs from the system's, and CDBA, which _must_ dynamically
# link to the Cadence-provided libstdc++, is used.
if(DEFINED $ENV{CDSHOME})
    list(PREPEND CMAKE_LIBRARY_PATH "$ENV{CDSHOME}/tools/cdsgcc/gcc/install/lib64")
endif()

install(TARGETS _gdstk
    COMPONENT _gdstk
    DESTINATION ${SKBUILD_PROJECT_NAME})

