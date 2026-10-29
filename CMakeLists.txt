cmake_minimum_required(VERSION 3.26)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake_modules")

# CMAKE_OSX_ARCHITECTURES must be set before project()
set(CMAKE_OSX_ARCHITECTURES "x86_64;arm64" CACHE STRING "Target architectures on macOS")

file(READ include/gdstk/gdstk.hpp HEADER_CONTENTS)
string(REGEX MATCH "GDSTK_VERSION \"([^\"]*)\"" _ ${HEADER_CONTENTS})
set(GDSTK_VERSION ${CMAKE_MATCH_1})

# Releases from this private fork include PEP 440 local
# version identifiers, but CMAKE only allows `[0-9.]` in
# the project version string.
string(REPLACE "+dd" "." GDSTK_VERSION ${GDSTK_VERSION})

# If building on a machine with an active Cadence install, use the
# Cadence-provided gcc and libstdc++.
#
# This prevents libstdc++ version conflicts when Florist loads both
# gdstk and CDBA, because CDBA must use the same compiler & libs as
# the Cadence installation does.
#
# The tool which invokes `cmake --build` must set `LD_LIBARY_PATH` to
# `${CDSHOME}/tools/cdsgcc/install/lib64`, so that the Cadence compiler can
# find its own libraries during the build. This is temporary and not needed
# to use the built gdstk wheel.
if(DEFINED ENV{CDSHOME})
    set(CMAKE_C_COMPILER "$ENV{CDSHOME}/tools/cdsgcc/gcc/install/bin/gcc")
    set(CMAKE_CXX_COMPILER "$ENV{CDSHOME}/tools/cdsgcc/gcc/install/bin/g++")

    list(PREPEND CMAKE_CXX_IMPLICIT_INCLUDE_DIRECTORIES "$ENV{CDSHOME}/tools/cdsgcc/gcc/install/include")
    list(PREPEND CMAKE_CXX_IMPLICIT_LINK_DIRECTORIES "$ENV{CDSHOME}/tools/cdsgcc/gcc/install/lib64")

    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -v")

    # Put the Cadence directory in the gdstk shared library's rpath. This
    # causes ld(1) to look there first when loading libraries, without having
    # to munge `LD_LIBRARY_PATH`.
    #
    # --disable-new-dtags causes GNU `ld` to write the rpath into the ELF `DT_RPATH`,
    # rather than `DT_RUNPATH`. The difference is that `DT_RPATH` cannot be overridden
    # at runtime by `LD_LIBRARY_PATH`.
    set(CMAKE_MODULE_LINKER_FLAGS "${CMAKE_MODULE_LINKER_FLAGS} -Wl,--disable-new-dtags -Wl,-rpath,$ENV{CDSHOME}/tools/cdsgcc/gcc/install/lib64")
endif()

project(gdstk
    VERSION ${GDSTK_VERSION}
    LANGUAGES CXX C)

if(CMAKE_PROJECT_NAME STREQUAL PROJECT_NAME)
    set(CMAKE_C_EXTENSIONS OFF)
    set(CMAKE_CXX_EXTENSIONS OFF)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
    set_property(GLOBAL PROPERTY USE_FOLDERS ON)
    include(CTest)
endif()

# Options
option(GDSTK_BUILD_EXAMPLES "Build C++ example programs" OFF)
if(CMAKE_PROJECT_NAME STREQUAL PROJECT_NAME)
    set(GDSTK_BUILD_EXAMPLES ON CACHE BOOL "Build C++ example programs" FORCE)
endif()

add_subdirectory(external)
add_subdirectory(src)

if(GDSTK_BUILD_EXAMPLES)
    add_subdirectory(docs/cpp)
endif()

if("${SKBUILD}" STREQUAL "2")
    add_subdirectory(python)
endif()
