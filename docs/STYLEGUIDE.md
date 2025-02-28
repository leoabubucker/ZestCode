# ZestCode Styleguide

> [!TIP]
> ZestCode is in the process of migrating to this new style, some older code may not yet be using this new style.

Maintaining a consistent coding style is important. It helps make the code more readable. ZestCode's style guide is largely inspired by [rustfmt](https://doc.rust-lang.org/stable/style-guide/).

## General Rules

> [!TIP]
> [clangd](https://marketplace.visualstudio.com/items?itemName=llvm-vs-code-extensions.vscode-clangd) can be used to automatically format your code using the ZestCode styleguide

Some basic rules are as follows:

- indent using 4 spaces, not tabs
- no more than 100 columns per line
- write tests for your code
- always use `enum class` over `enum`
- a `struct` should only have member variables, and no access modifiers
- don't use `typedef`, use `using` instead
- use [C++11 attributes](https://en.cppreference.com/w/cpp/language/attributes)
- only use macros as a last resort

For more details, see [.clang-format](../.clang-format).

## File extensions

> [!IMPORTANT]
> ZestCode is being rewritten in C++. No C files or headers may be added, but existing ones can be modified.

- C source files will have the extension `.c`
- C++ source files will have the extension `.cpp`
- C header files will have the extension `.h`
- C++ header files will have the extension `.hpp`
- Assembly source files will have the extension `.s`
- markdown documents will have the extension `.md`

## Naming Conventions

- **files, folders** - snake_case
- **classes, structs, enums, unions, concepts, etc** - PascalCase
- **functions** - snake_case
- **variables** - snake_case
- **member variable** - m_snake_case (not a typo)
- **macros** - SCREAMING_SNAKE_CASE
- **compile-time constants** - SCREAMING_SNAKE_CASE
- **enum members** - snake_case

## Documentation

Use Doxygen-style comments as shown in the sections below.

### File-Level Comments

These should be placed at the very start of a file.

```c
/**
 * @file filename.h
 *
 * @brief Short description of the file
 *
 * Extended description goes here. This should explain what the functions (etc)
 * in the file contains and a general description of what they do (no specifics,
 * but they should all have something in common anyway).
 *
 * This file should not be modified by users, since it gets replaced whenever
 * a kernel upgrade occurs.
 *
 * @copyright Copyright (c) 2017-2024, Purdue University ACM SIGBots.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
```

### Enum-Level Comments

These should be placed immediately before the declaration of the enum.

```c++
/*
 * @brief Short description of the enum
 *
 * Extended description of the enum goes here. This should explain general usage
 * patterns for the enum.
 */
enum class MyEnum {
        member_0, ///< short description of member 0 goes here.
        member_1, ///< these can be omitted if it's painfully obvious
        member_2, ///< what each is for, or if there are just so many of
        member_3, ///< them it doesn't make practical sense to
        member_4, ///< document them all.
}
```

> [!TIP]
> In the above example, the comments describing each member of the `enum` run together and form complete sentences for effect.
> Please do not do this in your code!

### Function-Level Comments

These should be placed immediately before the function prototype they are describing in a header file.

```c++
/**
 * @brief Brief description of the function.
 *
 * An extended description of the function (if applicable).
 *
 * This function uses the following values of errno when an error state is
 * reached:
 * ERRNO_VALUE - Description of what causes this error
 *
 * @tparam T the type of the parameters
 *
 * @param parameter_name The parameter description
 * @param other_parameter_name The parameter description
 *
 * @return The description of the return value, if this is longer than one line
 * then it will wrap around under the return statement
 *
 * @code
 * // example code here
 * @endcode
 *
 * @see src/referenced_file.cpp
 */
```

### Inline Implementation Comments

Sometimes it is necessary to explain a particularly complex statement or series of statements. In this case, you should use inline comments, placed either immediately before or trailing the line or lines in question. In general, prefer placing such comments before offending lines, unless the comment is quite short. These comments should start with a `//` followed by a space. If they are placed trailing a line, they should be separated from the end of the line by one space.

```c++
float Q_rsqrt(float number) {
    long i;
    float x2, y;
    const float threehalfs = 1.5F;
    x2 = number * 0.5F;
    y  = number;
    // perform some absolute magic on these numbers to get the inverse square root
    i  = *(long*)&y; // evil floating point bit level hacking
    i  = 0x5f3759df - (i >> 1); // what the [heck]?
    y  = *(float*)&i;
    y  = y * (threehalfs - (x2 * y * y)); // 1st iteration
    //y  = y * (threehalfs - (x2 * y * y)); // 2nd iteration, this can be removed
    return y;
}
```
> [!TIP]
> In the above example, there is a line of code that has been commented out.
> This is fine to do while testing, but any commented out lines of code should be removed before any merge into the master branch takes place, unless a compelling reason can be presented for them to remain.

All that being said, try to avoid code that is so complex that it requires inline comments for its purpose to be clear.

#### Notes to Other Developers (Or Yourself)

When writing code, it can sometimes be useful to leave notes to other developers or to yourself in the future. Examples of these include:

- `// TODO: something that should be done`
- `// HACK: used to describe a particularly nasty way of solving a problem-- could be improved, but it works for now`

While it is not strictly necessary to use these keywords in comments, they can be helpful-- modern editors either highlight some of these keywords by default or have extensions that do.
This can make certain comments stand out even more when developers are "grepping" the codebase (visually or otherwise).