# rotate-canvas

Simple library to rotate canvas image using javascript. You can rotate image by 90, 180 or 270 degrees. Passing any other value will draw image/video without any rotation


## Installation

To install run:

```bash
yarn add rotate-canvas
# or
npm i rotate-canvas
```

## Example

```js
import { drawRotated } from 'deviceorientation'

let video = document.querySelector('#video');
let canvas = document.querySelector('#canvas');
canvas.height = video.videoHeight;
canvas.width = video.videoWidth;
let ctx = canvas.getContext("2d");

drawRotated(video, canvas, ctx, 180);
```