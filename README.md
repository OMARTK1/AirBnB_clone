This is the console for the web application AirBnB.
in this project:

creation of a parent class (called BaseModel) to take care of the initialization, serialization and deserialization of future instances
creation of a simple flow of serialization/deserialization: Instance <-> Dictionary <-> JSON string <-> file
creation of all classes used for AirBnB (User, State, City, Place…) that inherit from BaseModel
creation of the first abstracted storage engine of the project: File storage.
creation of all unittests to validate all classes and storage engine