# Box Wireframe Renderer

## Repository
https://github.com/bpj6g5c5ts-ops/ANGM-2305.0W2-final-project

## Description
My final project will be a 3d box wireframe renderer that takes in the intended fov/focal length of the camera, rotation of the box, position of any one of the vertex on the screen, its distance from the camera, and the dimension of the box, then render out a wireframe of the box with proper perspective. It will basically be a seudo 3d program, and the resulting wireframe can then be used as a guide for perspective drawing in art programs such as Krita, which have file layers that syncs with a target image and will auto update when the image is edited. 

## Features
- Camera fov calculator
    - Calculates the fov of the camera based on sensor dimention and focal length
- Forsortening calculator
    - Accepts a length and distance value and calculate the forshortened length in pixels based on the camera spec. Can also do the reverse: accepts a length in meters and length in pixels and outputs the distance. 
- Box vertex coordinate calculator
    - Calculates each vertex coordinate (in pixels) of the box based on user settings:
        - dimention of the box
        - rotation angle around all 3 axis
        - distance given (from the origin)
        - camera specs (focal length or fov, resolution, and sensor dimension)
        - origin point of the box (top left front corner, center, bottom right back corner, etc)
- Box draw
    - Draws the box with the 8 corner vertices and the lines connecting them.
- (Optional) Krita plugin
    - This might be too ambitious, but if possible, I will make it available as a krita python plugin with a UI and menu for editing the settings

## Challenges
- Know the math behind rectilinear projection.
- Know how to make a krita python plugin (Optional).

## Outcomes
Ideal Outcome:
- Have a fully functional Krita plugin with a UI and allows the user to move and rotate the box in real time

Minimal Viable Outcome:
- Have a python program that saves an image of the wireframe to a folder which can then be linked to a Krita file layer

## Milestones

- Week 1
    1. Implement camera fov calculator
    2. Implement Forshortening calculator

- Week 2
    1. Implement Box cordinate calculator
    2. Implement Box draw

- Week N
    1. Debugging
    2. Adding extra features
    3. Make it into a Krita plugin (If time permits)
