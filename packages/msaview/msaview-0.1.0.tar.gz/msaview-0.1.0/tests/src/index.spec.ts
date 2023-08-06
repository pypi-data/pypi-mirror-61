// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import expect = require('expect.js');

import {
  // Add any needed widget imports here (or from controls)
} from '@jupyter-widgets/base';

import {
  createTestModel
} from './utils.spec';

import {
  MSAModel, MSAView
} from '../../src/'


describe('Example', () => {

  describe('MSAModel', () => {

    it('should be createable', () => {
      let model = createTestModel(MSAModel);
      expect(model).to.be.an(MSAModel);
      expect(model.get('value')).to.be('Hello World');
    });

    it('should be createable with a value', () => {
      let state = { value: 'Foo Bar!' }
      let model = createTestModel(MSAModel, state);
      expect(model).to.be.an(MSAModel);
      expect(model.get('value')).to.be('Foo Bar!');
    });

  });

});
