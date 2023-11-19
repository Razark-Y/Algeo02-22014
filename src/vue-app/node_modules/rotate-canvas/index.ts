export function drawRotated(source: CanvasImageSource, canvas: HTMLCanvasElement, context: CanvasRenderingContext2D, degrees: number){
    const width = canvas.width
    const height = canvas.height

    if (degrees === 90 || degrees === 270) {
        canvas.width = height
        canvas.height = width
    }

    if (degrees === 90) {
        context.translate(height,0);
    } else if (degrees === 180) {
        context.translate(width,height);
    } else if (degrees === 270) {
        context.translate(0,width);
    } else {
        context.translate(0,0);
    }

    context.rotate(degrees*Math.PI/180);

    context.drawImage(source,-source.width/2,-source.width/2, width, height);
}

export default {
    drawRotated,
}