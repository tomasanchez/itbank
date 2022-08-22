/**
 * Model.js
 *
 * @file a Generic Model implementation.
 * @author Tomás Sánchez
 * @since  06.12.2022
 */

class Model {
  constructor(data = {}) {
    this.data = {};
  }

  /**
   * Gets the property value.
   * @param {string} key the poperty key
   * @return {string} the property value
   */
  getProperty(key) {
    return this.data[key];
  }

  /**
   * Sets a property into the model.
   *
   * @param {string} key the poperty accessor
   * @param {string} value the assigned string
   * @returns {Model} the Model instance
   */
  setProperty(key, value) {
    this.data[key] = value;
    return this;
  }
}
