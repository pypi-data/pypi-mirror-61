Changelog
=========

0.0.2 (2020-02-20)
-------------------

- Added the ability to create a JSONObject property directly from the class.
- Properties can now be reused between JSON objects, as long as the attribute
  name stays the same.
- ConstantProperty and EnumProperty can now report their values.
- StaticJSONValidator can now cache schema/validators for unhashable objects.
- Pretty serialisation.
- Can query the optionality of a property.
- Can specify initial values by attribute name.
- Can see if the class OR an instance has a property (instances include additional
  properties).
- Iterating over properties now only iterates over the names, and can be done on the
  class or an instance, as above.
- Sub-types can pass programmatic properties in __init_subclass__.

0.0.1 (2020-02-20)
-------------------

- Initial release
