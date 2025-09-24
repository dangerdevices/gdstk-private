cmake_minimum_required(VERSION 3.26)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake_modules")

file(READ include/gdstk/gdstk.hpp HEADER_CONTENTS)
string(REGEX MATCH "GDSTK_VERSION \"([^\"]*)\"" _ ${HEADER_CONTENTS})
set(GDSTK_VERSION ${CMAKE_MATCH_1})

# Releases from this private fork include PEP 440 local
# version identifiers, but CMAKE only allows `[0-9.]` in
# the project version string.
string(REPLACE "+dd" "." GDSTK_VERSION ${GDSTK_VERSION})

if(DEFINED ENV{CDSHOME})
    set(CMAKE_C_COMPILER "$ENV{CDSHOME}/tools/cdsgcc/gcc/install/bin/gcc")
    set(CMAKE_CXX_COMPILER "$ENV{CDSHOME}/tools/cdsgcc/gcc/install/bin/g++")

    list(PREPEND CMAKE_CXX_IMPLICIT_INCLUDE_DIRECTORIES "$ENV{CDSHOME}/tools/cdsgcc/gcc/install/include")
    list(PREPEND CMAKE_CXX_IMPLICIT_LINK_DIRECTORIES "$ENV{CDSHOME}/tools/cdsgcc/gcc/install/lib64")

    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -v")
    set(CMAKE_MODULE_LINKER_FLAGS "${CMAKE_MODULE_LINKER_FLAGS} -Wl,-rpath,$ENV{CDSHOME}/tools/cdsgcc/gcc/install/lib64")

    # TODO: This does not work.
    # set(ENV{LD_LIBRARY_PATH}, "$ENV{CDSHOME}/tools/cdsgcc/install/lib64")
endif()

project(gdstk
    VERSION ${GDSTK_VERSION}
    LANGUAGES CXX C)

set(CMAKE_OSX_ARCHITECTURES "x86_64;arm64" CACHE STRING "Target architectures on macOS")

if(CMAKE_PROJECT_NAME STREQUAL PROJECT_NAME)
    set(CMAKE_C_EXTENSIONS OFF)
    set(CMAKE_CXX_EXTENSIONS OFF)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

    set_property(GLOBAL PROPERTY USE_FOLDERS ON)

    if (CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /nologo /W3 /MD /EHsc /wd4996")
        set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /Zi")
        set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /Ox /GL -DNDEBUG")
    else()
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wshadow -Wvla -Wformat -Wno-missing-field-initializers -Wno-missing-braces -Wno-cast-function-type -Wno-unused-parameter")
        set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g")
        set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -DNDEBUG")
    endif()

    include(CTest)
    add_subdirectory(docs/cpp)
endif()

if(APPLE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mmacosx-version-min=10.9")
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mmacosx-version-min=10.9")
    set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -undefined dynamic_lookup -flat_namespace")
endif()

add_subdirectory(external)
add_subdirectory(src)

if("${SKBUILD}" STREQUAL "2")
    add_subdirectory(python)
endif()

