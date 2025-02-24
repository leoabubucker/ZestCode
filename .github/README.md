# ZestCode

ZestCode is a truly open-source framework for the VEX V5. It's a PROS fork, and exists to address some PROS issues, particularly in reliability, tooling, and community input.

### FAQ

> Why can ZestCode be compiled from source, but PROS can't?

PROS depends on `libv5rts`, which is a private version of the VEX SDK. ZestCode depends on `libv5rt.a`, which is public.

<br>

> Is ZestCode legal?

Yup, 100% legal. It is not prohibited in the V5RC, VURC, or VAIRC game manual, and it's legal from a copyright standpoint.

<br>

### Specs (WIP)

#### API

- PROS compatible API
  - directly for now
  - indirectly through a translation layer in future
- VEXCode compatible API
  - indirectly through a translation layer (maybe)

#### Scheduler

- [FreeRTOS](https://www.freertos.org/)
- Preemptive scheduling as an advanced feature
- Cooperative scheduling

#### Build Tools

- [CMake](https://cmake.org/) for build script
  - easy integration with other build tools
  - a much more readable build script
- [vcpkg](https://vcpkg.io/en/) for package management
  - far more advanced than PROS branchline
- [LLVM](https://llvm.org/) for compiler tools
  - faster compiling and linking
  - friendlier error and warning messages

#### System Libraries

- [Newlib libm and libc](https://sourceware.org/newlib/)
- The public VEX V5 SDK distributed with VEXCode

### Acknowledgements

The authors of ZestCode would like to thank the developers of PROS for their years of service, and for paving the way for alternatives like ZestCode to even exist in the first place. We'd also like to thank the developers of Vexide, ZestCode wouldn't exist if not for their feats
