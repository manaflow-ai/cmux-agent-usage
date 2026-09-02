"use strict";

const networkDisabled = () =>
  Promise.reject(new Error("Network access is disabled for Agent Usage."));

Object.defineProperty(globalThis, "fetch", {
  configurable: false,
  enumerable: true,
  value: networkDisabled,
  writable: false,
});
