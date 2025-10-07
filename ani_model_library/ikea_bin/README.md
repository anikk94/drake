Ikea bin model
==============

This package contains a simple SDF model that references a glTF asset:

- `ikea_bin.sdf` - SDF model which references `assets/ikea_bin.gltf`.
- `assets/ikea_bin.gltf` - visual mesh used by the SDF.

Using with Bazel
----------------
There is a small `sh_binary` target `//ani_model_lib/ikea_bin:print_runfiles`
that stages the SDF and glTF as runfiles. Use it to verify that Bazel
staged the asset correctly before launching a simulation.

Example:

```bash
bazel run //ani_model_lib/ikea_bin:print_runfiles
```

How the SDF references the mesh
-------------------------------
The SDF uses a package-style URI `model://ikea_bin/assets/ikea_bin.gltf`.
When using Drake's model parsers together with Bazel run, Bazel will stage
package data into the runfiles and Drake will be able to locate the asset
relative to the package name. If you load the SDF directly from the
filesystem (outside of Bazel), ensure the `assets/ikea_bin.gltf` is present
next to the SDF or update the URI to a local file:// path.

If you want help wiring this into a specific simulation target, tell me
which example or binary you use and I can add a small demo `sh_binary` or
update a WORKSPACE rule to make the model importable.
