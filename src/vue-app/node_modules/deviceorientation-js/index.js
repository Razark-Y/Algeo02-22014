let _deviceOrientation_cachedEvent;

export default {
    /**
     * @param {DeviceOrientationEvent} event
     * @param {Boolean} exactAngle - If it is set to true, then return a number from 0 up to 360, which represents current angle (rounded), otherwise it only returns 0, 90, 180 or 270 depending on which is more close to the current device angle
     * @returns {Number} current angle of device, see exactAngle description for more details
     */
    getDeviceOrientation: function (event, exactAngle = false) {
        if ( ! event && ! _deviceOrientation_cachedEvent) {
            return 0  
        } else if ( ! event) {
            event = _deviceOrientation_cachedEvent
        }

        if ( ! event || ! event.beta || ! event.gamma) {
            return 0
        }

        // shoutout to https://stackoverflow.com/a/40720543
        const x = event.beta;  // In degree in the range [-180,180], x, 'front to back'
        const y = event.gamma; // In degree in the range [-90,90], y, 'left to right'
      
        // calculate the angle
        const rad = Math.atan2(y, x);
        let deg = rad * (180 / Math.PI);
      
        // take into account if phone is held sideways / in landscape mode
        const screenOrientation = screen.orientation || screen.mozOrientation || screen.msOrientation;
        // 90, -90, or 0
        const angle = screenOrientation.angle || window.orientation || 0; 
        
        // now deg is <-180,180>
        deg = Math.round(deg + angle);
        // so if its negative, we will convert it to <180,360>
        if (deg < 0) {
            deg = 360 + deg
        }

        if (exactAngle) {
            return deg
        }

        // should be 45 instead of 55, but its more preferable to keep default (portrait mode)
        if (deg > 55 && deg <= 135) {
            return 90
        }

        if (deg > 135 && deg < 225) {
            return 180
        }

        // should be 315 instead of 305, but its more preferable to keep default (portrait mode)
        if (deg >= 225 && deg < 305) {
            return 270
        }

        return 0
    },

    /**
     * @returns {Boolean} Returns true if device is in portrait mode, false otherwise
     */
    isPortrait(event) {
        const orientation = this.getDeviceOrientation(event);
        return (orientation === 0 || orientation === 180)
    },

    /**
     * @returns {Boolean} Returns true if device is in landscape (flipped to side) mode, false otherwise
     */
    isLandscape(event) {
        const orientation = this.getDeviceOrientation(event);
        return (orientation === 90 || orientation === 270)
    },

    /**
     * @returns {Boolean} Returns true if device is in standard portrait mode, false otherwise
     */
    isPortraitDefault(event) {
        return this.getDeviceOrientation(event) === 0
    },

    /**
     * @returns {Boolean} Returns true if device is in reverse portrait mode, false otherwise
     */
    isPortraitReversed(event) {
        return this.getDeviceOrientation(event) === 180
    },

    /**
     * @returns {Boolean} Returns true if device is in landscape (flipped to right side) position, false otherwise
     */
    isLandscapeRight(event) {
        return this.getDeviceOrientation(event) === 90
    },

    /**
     * @returns {Boolean} Returns true if device is in landscape (flipped to left side) position, false otherwise
     */
    isLandscapeLeft(event) {
        return this.getDeviceOrientation(event) === 270
    },

    /**
     * Sets `deviceorientation` listener for you, the last event will be cached, so you can call `getDeviceOrientation` without any parameter and the cached event will be used
     * 
     * @param {Boolean} throwErrorIfNotSupported if sets to true, then it will throw an error if window.DeviceOrientationEvent is undefined
     */
    init(throwErrorIfNotSupported = false) {
        if (window.DeviceOrientationEvent === undefined) {
            if (throwErrorIfNotSupported) {
                throw new Error('DeviceOrientationEvent is not supported in current browser')
            }
            return
        }
        window.addEventListener("deviceorientation", (event) => {
            _deviceOrientation_cachedEvent = event
        }, true);
    },
}