# 3D Gaussian Ray Tracing in Blender

A Blender implementation of the **3D Gaussian Ray Tracing** rendering technique using Geometry Nodes and Shader Nodes, enabling raytracing of Gaussian splats directly within Blender's Cycles renderer.

## Overview ℹ️

This project implements the rendering engine described in the research paper [**"3D Gaussian Ray Tracing: Fast Tracing of Particle Scenes"**](https://arxiv.org/abs/2407.07090) by Moenne-Loccoz et al. (2024). It allows you to raytrace 3D Gaussian splats natively in Blender using Cycles, and leverage Gaussian splatting in a potential VFX pipeline.

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="images/Rasterized.png" alt="Rasterized Gaussian Splatting" width="400"/>
        <br/>
        <b>Rasterized Rendering</b>
        <br/>
        <em>Traditional Gaussian splatting rasterization</em>
      </td>
      <td align="center">
        <img src="images/Raytraced.png" alt="Raytraced Gaussian Splatting" width="400"/>
        <br/>
        <b>Raytraced Rendering</b>
        <br/>
        <em>3D Gaussian ray tracing with Cycles. Same scene + additional glossy and glass spheres.</em>
      </td>
    </tr>
  </table>
</div>

The main feature of this technique is indeed to me the possibility to handle reflections, refractions, motion blur, bokeh with gaussian splatting precision.

One can notice that the reconstruction is not similar compared to the rasterized version. Indeed, i should ghave finetuned the GS scene with a raytracer rendering engine like Moenne-Loccoz et al. (2024) suggest.

## Use-case exemple 💡

Here is a use case I though of for this technique : integration of a glossy 3D object that moves between detailed object.
In this context, a rough rotoscopie does not provide enough detail while an HDRI would not allow the sphere to move freely through the scene. 
Thus It seems to me that raytracing gaussian splats is in this context one of the best pipeline one can come up with.


### Pipeline description 🛠️

#### On set 🎬
1. Shoot 📸
2. Scan the scene 📡 (don't forget the ceiling like I did)

#### Post Production 🖥️
3. Track the scene in Blender 🔎
4. Train the Gaussian splatting scene
5. Align the GS scene to the track in Blender (one can use the provided `align_transform.py` script)
6. Render the glossy element 🎞️
7. Compose the original shot with the 3D rendered glossy element

## Usage 🧭

### Import the material and geometry 📥
1. Clone or download this repository:
    ```bash
    git clone <your-repo-url>
    ```

2. From Blender, use File → Append and select

3. Find the downloaded `Gaussian_Raytraced.blend`

4. Select:
    - `Splat_Shader` in the Material folder
    - `Splat_Geometry` in the NodeTree folder

### Apply on a pre-trained Gaussian splatting scene 📂

5. Use File → Import → Stanford PLY (.ply) to import a pre-trained Gaussian splatting scene

6. Assign the `Splat_Shader` material and the `Splat_Geometry` geometry node tree.

### Render 🎛️

7. Make sure to use Cycles

8. In the "Light Path" Cycles parameters, increase "Transparent" to 1024

9. The point cloud is now ready to be rendered directly with Cycles, interacting with any other object in the scene.


### Node Setup Explanation 🧩

#### Geometry Nodes 🧩
For each point in the point cloud, the geometry node tree:
- Creates an IcoSphere
- Moves, scales and rotates it according to .ply data
- Adapts these transformations according to Blender's object properties
- Provides this information to the shader node tree
- Applies the proper shader.


#### Shader Nodes 🎨
For each ray crossing an IcoSphere, the shader node:
- Computes the maximum opacity on its path according to Moenne-Loccoz et al. (2024)
- Computes color according to ray directions

I did not implement Blender object rotation influence over ray-direction management, thus only the first order of spherical harmonics works for now.


### Limitations ⚠️

- The actual Moenne-Loccoz et al. (2024) implementation includes instancing and shadow projections which this Cycles implementation does not.
- As explained in Moenne-Loccoz et al. (2024), each scene should be fine-tuned with a ray-tracing rendering method in order to be as accurate as possible with this rendering method.
- Rendering is far from real-time. The provided example frame was rendered on an RTX 3080 in 2 minutes and 30 seconds. (Most of the time is actually used to compute BVH and load everything in memory.) I recommend using a Gaussian rasterization addon to set up the scene and only use ray-tracing for final rendering.

## References 📚

- **Original Paper**: Moenne-Loccoz, N., Mirzaei, A., Perel, O., de Lutio, R., Martinez Esturo, J., State, G., Fidler, S., Sharp, N., & Gojcic, Z. (2024). *3D Gaussian Ray Tracing: Fast Tracing of Particle Scenes*. arXiv:2407.07090 [cs.GR]. [https://arxiv.org/abs/2407.07090](https://arxiv.org/abs/2407.07090)
- **3D Gaussian Splatting**: Kerbl, B., Kopanas, G., Leimkühler, T., & Drettakis, G. (2023). "3D Gaussian Splatting for Real-Time Radiance Field Rendering." ACM Transactions on Graphics (SIGGRAPH Conference Proceedings), 42(4), July 2023. http://www-sop.inria.fr/reves/Basilic/2023/KKLD23
- **Blender Cycles**: [Official Cycles Documentation](https://docs.blender.org/manual/en/latest/render/cycles/index.html)

