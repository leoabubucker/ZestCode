.. ZestCode documentation master file

Welcome to ZestCode's documentation!
====================================
.. attention::
    ZestCode is under heavy development, and we'd greatly appreciate any contributors! Consider joining our `Discord Server <https://discord.gg/vNMXCvVwdY>` if you are interested.

    ZestCode is a truly open-source framework for the VEX V5. It's a PROS fork, and exists to address some PROS issues, particularly in reliability, tooling, and community input.

WIP Why ZestCode?
----------------------- ------------
- [X] designed to be easy to contribute to
- [X] can be built from source
- [X] public development discussions and decision making
- [ ] superior contributor documentation
- [ ] superior build system
- [ ] more understandable compiler errors/warnings
- [ ] faster build times
- [ ] smarter package management
- [ ] deterministic builds

FAQ
-----------------------------------
.. admonition:: Is ZestCode Legal?
    Yup, 100% legal. It is not prohibited in the V5RC, VURC, or VAIRC game manual, and it's legal from a copyright standpoint.

.. admonition:: Why Can ZestCode Be Compiled From Source, But PROS Can't?
    PROS depends on _libv5rts_, which is a private version of the VEX SDK. ZestCode depends on _libv5rta_, which is public.

License
-----------------------------------
`Mozilla Public License 2.0 <../LICENSE>`

Contributing
-----------------------------------
`CONTRIBUTING.md <CONTRIBUTING.md>`

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api_reference
   contributing
   changelog

Acknowledgements
-----------------------------------
The authors of ZestCode would like to thank the developers of PROS for their years of service, and for paving the way for alternatives like ZestCode to even exist in the first place. We'd also like to thank the developers of vexide, ZestCode wouldn't exist if not for their feats.

API Reference
====================================
.. doxygenindex::
