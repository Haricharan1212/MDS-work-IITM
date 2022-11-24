import mujoco

XML=r"""
<mujoco>
  <asset>
    <mesh file="gizmo.stl"/>
  </asset>
  <worldbody>
    <body>
      <freejoint/>
      <geom type="mesh" name="gizmo" mesh="gizmo"/>
    </body>
  </worldbody>
</mujoco>
"""

print(help(mujoco))

ASSETS=dict()
with open('Menger_sponge_sample.stl', 'rb') as f:
    ASSETS['gizmo.stl'] = f.read()

model = mujoco.MjModel.from_xml_string(XML, ASSETS)
data = mujoco.MjData(model)
while data.time < 1:
  mujoco.mj_step(model, data)
  print(data.geom_xpos)