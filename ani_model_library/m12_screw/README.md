M12 screw models
=================

This folder contains models for an M12 metric socket-head screw.

Files:
- `m12_screw.sdf` - original model that references an externally-provided mesh (gltf).
- `m12_screw_gpt.sdf` - a simple native SDF model that approximates the screw with
  two cylinders (shaft and head). Units are meters (m) and kilograms (kg).

Notes:
- The `m12_screw_gpt.sdf` is intended as a lightweight primitive-only model
  for quick simulation or collision testing. Dimensions are approximate and
  chosen to resemble a common M12 socket-head cap screw (shaft: 12 mm dia,
  50 mm long; head: 18 mm dia, 10 mm tall).
- Inertial properties are approximate; for high-fidelity dynamics use a
  measured mesh or CAD export.
