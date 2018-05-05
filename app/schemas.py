#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Integer()
    username = fields.Str()
    email = fields.Email()
    first_name = fields.Str()
    full_name = fields.Str()
