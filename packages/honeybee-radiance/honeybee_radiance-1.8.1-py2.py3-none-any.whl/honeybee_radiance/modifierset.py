"""Radiance modifier set."""
from __future__ import division

from honeybee_radiance.modifier import Modifier
from honeybee_radiance.lib.modifiers import generic_floor, generic_wall, \
    generic_ceiling, generic_door, generic_exterior_window, generic_interior_window, \
    generic_exterior_shade, generic_interior_shade, air_wall

from honeybee._lockable import lockable
from honeybee.typing import valid_rad_string


_default_modifiers = {
    '_BaseSet': {'exterior': None, 'interior': None},
    'WallSet': {
        'exterior': generic_wall,
        'interior': generic_wall
    },
    'FloorSet': {
        'exterior': generic_floor,
        'interior': generic_floor
    },
    'RoofCeilingSet': {
        'exterior': generic_ceiling,
        'interior': generic_ceiling
    },
    'ApertureSet': {
        'exterior': generic_exterior_window,
        'interior': generic_interior_window,
        'operable': generic_exterior_window,
        'skylight': generic_exterior_window
    },
    'DoorSet': {
        'exterior': generic_door,
        'interior': generic_door,
        'exterior_glass': generic_exterior_window,
        'interior_glass': generic_interior_window,
        'overhead': generic_door
    },
    'ShadeSet': {
        'exterior': generic_exterior_shade,
        'interior': generic_interior_shade
    }
}


@lockable
class ModifierSet(object):
    """Set containting all radiance modifiers needed to create a radiance model.

    ModifierSets can be used to establish templates that are applied broadly
    across a Model, like a color scheme used consistently throughout a building.

    Properties:
        * name
        * wall_set
        * floor_set
        * roof_ceiling_set
        * aperture_set
        * door_set
        * shade_set
        * air_wall_modifier
        * modifiers
        * modified_modifiers
        * modifiers_unique
        * modified_modifiers_unique
    """

    __slots__ = ('_name', '_wall_set', '_floor_set', '_roof_ceiling_set',
                 '_aperture_set', '_door_set', '_shade_set', '_air_wall_modifier',
                 '_locked')

    def __init__(self, name, wall_set=None, floor_set=None, roof_ceiling_set=None,
                 aperture_set=None, door_set=None, shade_set=None,
                 air_wall_modifier=None):
        """Initialize radiance modifier set.

        Args:
            name: Text string for modifier set name.
            wall_set: An optional WallSet object for this ModifierSet.
                If None, it will be the honeybee generic default WallSet.
            floor_set: An optional FloorSet object for this ModifierSet.
                If None, it will be the honeybee generic default FloorSet.
            roof_ceiling_set: An optional RoofCeilingSet object for this ModifierSet.
                If None, it will be the honeybee generic default RoofCeilingSet.
            aperture_set: An optional ApertureSet object for this ModifierSet.
                If None, it will be the honeybee generic default ApertureSet.
            door_set: An optional DoorSet object for this ModifierSet.
                If None, it will be the honeybee generic default DoorSet.
            shade_set: An optional ShadeSet object for this ModifierSet.
                If None, it will be the honeybee generic default ShadeSet.
            air_wall_modifier: An optional Modifier to be used for all Faces with
                an AirWall face type. If None, it will be the honyebee generic
                air wall modifier.
        """
        self._locked = False  # unlocked by default
        self.name = name
        self.wall_set = wall_set
        self.floor_set = floor_set
        self.roof_ceiling_set = roof_ceiling_set
        self.aperture_set = aperture_set
        self.door_set = door_set
        self.shade_set = shade_set
        self.air_wall_modifier = air_wall_modifier

    @property
    def name(self):
        """Get or set a text string for modifier set name."""
        return self._name

    @name.setter
    def name(self, name):
        self._name = valid_rad_string(name, 'ModifierSet name')

    @property
    def wall_set(self):
        """Get or set the WallSet assigned to this ModifierSet."""
        return self._wall_set

    @wall_set.setter
    def wall_set(self, value):
        if value is not None:
            assert isinstance(value, WallSet), \
                'Expected WallSet. Got {}'.format(type(value))
            self._wall_set = value
        else:
            self._wall_set = WallSet()

    @property
    def floor_set(self):
        """Get or set the FloorSet assigned to this ModifierSet."""
        return self._floor_set

    @floor_set.setter
    def floor_set(self, value):
        if value is not None:
            assert isinstance(value, FloorSet), \
                'Expected FloorSet. Got {}'.format(type(value))
            self._floor_set = value
        else:
            self._floor_set = FloorSet()

    @property
    def roof_ceiling_set(self):
        """Get or set the RoofCeilingSet assigned to this ModifierSet."""
        return self._roof_ceiling_set

    @roof_ceiling_set.setter
    def roof_ceiling_set(self, value):
        if value is not None:
            assert isinstance(value, RoofCeilingSet), \
                'Expected RoofCeilingSet. Got {}'.format(type(value))
            self._roof_ceiling_set = value
        else:
            self._roof_ceiling_set = RoofCeilingSet()

    @property
    def aperture_set(self):
        """Get or set the ApertureSet assigned to this ModifierSet."""
        return self._aperture_set

    @aperture_set.setter
    def aperture_set(self, value):
        if value is not None:
            assert isinstance(value, ApertureSet), \
                'Expected ApertureSet. Got {}'.format(type(value))
            self._aperture_set = value
        else:
            self._aperture_set = ApertureSet()

    @property
    def door_set(self):
        """Get or set the DoorSet assigned to this ModifierSet."""
        return self._door_set

    @door_set.setter
    def door_set(self, value):
        if value is not None:
            assert isinstance(value, DoorSet), \
                'Expected DoorSet. Got {}'.format(type(value))
            self._door_set = value
        else:
            self._door_set = DoorSet()

    @property
    def shade_set(self):
        """Get or set the ShadeSet assigned to this ModifierSet."""
        return self._shade_set

    @shade_set.setter
    def shade_set(self, value):
        if value is not None:
            assert isinstance(value, ShadeSet), \
                'Expected ShadeSet. Got {}'.format(type(value))
            self._shade_set = value
        else:
            self._shade_set = ShadeSet()

    @property
    def air_wall_modifier(self):
        """Get or set a Modifier to be used for all Faces with an AirWall face type."""
        if self._air_wall_modifier is None:
            return air_wall
        return self._air_wall_modifier

    @air_wall_modifier.setter
    def air_wall_modifier(self, value):
        if value is not None:
            assert isinstance(value, Modifier), \
                'Expected Modifier. Got {}'.format(type(value))
            value.lock()   # lock editing in case modifier has multiple references
        self._air_wall_modifier = value

    @property
    def modifiers(self):
        """List of all modifiers contained within the set."""
        return self.wall_set.modifiers + \
            self.floor_set.modifiers + \
            self.roof_ceiling_set.modifiers + \
            self.aperture_set.modifiers + \
            self.door_set.modifiers + \
            self.shade_set.modifiers + \
            [self.air_wall_modifier]

    @property
    def modified_modifiers(self):
        """List of all modifiers that are not defaulted within the set."""
        modified_modifiers = self.wall_set.modified_modifiers + \
            self.floor_set.modified_modifiers + \
            self.roof_ceiling_set.modified_modifiers + \
            self.aperture_set.modified_modifiers + \
            self.door_set.modified_modifiers + \
            self.shade_set.modified_modifiers
        if self._air_wall_modifier is not None:
            modified_modifiers.append(self._air_wall_modifier)
        return modified_modifiers

    @property
    def modifiers_unique(self):
        """List of all unique modifiers contained within the set."""
        return list(set(self.modifiers))

    @property
    def modified_modifiers_unique(self):
        """List of all unique modifiers that are not defaulted within the set."""
        return list(set(self.modified_modifiers))

    def get_face_modifier(self, face_type, boundary_condition):
        """Get a modifier object that will be assigned to a given type of face.

        Args:
            face_type: Text string for the type of face (eg. 'Wall', 'Floor',
                'Roof', 'AirWall').
            boundary_condition: Text string for the boundary condition
                (eg. 'Outdoors', 'Surface', 'Ground')
        """
        if face_type == 'Wall':
            return self._get_modifier_from_set(self.wall_set, boundary_condition)
        elif face_type == 'Floor':
            return self._get_modifier_from_set(self.floor_set, boundary_condition)
        elif face_type == 'RoofCeiling':
            return self._get_modifier_from_set(self.roof_ceiling_set, boundary_condition)
        elif face_type == 'AirWall':
            return self.air_wall_modifier
        else:
            raise NotImplementedError(
                'Face type {} is not recognized for ModifierSet'.format(face_type))

    def get_aperture_modifier(self, boundary_condition, is_operable, parent_face_type):
        """Get a modifier object that will be assigned to a given type of aperture.

        Args:
            boundary_condition: Text string for the boundary condition
                (eg. 'Outdoors', 'Surface')
            is_operable: Boolean to note whether the aperture is operable.
            parent_face_type: Text string for the type of face to which the aperture
                is a child (eg. 'Wall', 'Floor', 'Roof').
        """
        if boundary_condition == 'Outdoors':
            if not is_operable:
                if parent_face_type == 'Wall':
                    return self.aperture_set.window_modifier
                else:
                    return self.aperture_set.skylight_modifier
            else:
                return self.aperture_set.operable_modifier
        elif boundary_condition == 'Surface':
            return self.aperture_set.interior_modifier
        else:
            raise NotImplementedError(
                'Boundary condition {} is not recognized for apertures in '
                'ModifierSet'.format(boundary_condition))

    def get_door_modifier(self, boundary_condition, is_glass, parent_face_type):
        """Get a modifier object that will be assigned to a given type of door.

        Args:
            boundary_condition: Text string for the boundary condition
                (eg. 'Outdoors', 'Surface').
            is_glass: Boolean to note whether the door is glass (instead of opaque).
            parent_face_type: Text string for the type of face to which the door
                is a child (eg. 'Wall', 'Floor', 'Roof').
        """
        if boundary_condition == 'Outdoors':
            if not is_glass:
                if parent_face_type == 'Wall':
                    return self.door_set.exterior_modifier
                else:
                    return self.door_set.overhead_modifier
            else:
                return self.door_set.exterior_glass_modifier
        elif boundary_condition == 'Surface':
            if not is_glass:
                return self.door_set.interior_modifier
            else:
                return self.door_set.interior_glass_modifier
        else:
            raise NotImplementedError(
                'Boundary condition {} is not recognized for doors in '
                'ModifierSet'.format(boundary_condition)
                )

    def get_shade_modifier(self, is_indoor=False):
        """Get a modifier object that will be assigned to a shade.

        Args:
            is_indoor: A boolean to indicate if the shade is on the indoors or
                the outdoors of its parent. Default: False.
        """
        if is_indoor:
            return self.shade_set.interior_modifier
        else:
            return self.shade_set.exterior_modifier

    @classmethod
    def from_dict(cls, data):
        """Create a ModifierSet from a dictionary.

        Note that the dictionary must be a non-abridged version for this
        classmethod to work.

        Args:
            data: Dictionary describing the ModifierSet.
        """
        assert data['type'] == 'ModifierSet', \
            'Expected ModifierSet. Got {}.'.format(data['type'])
        
        try:  # ensure the putil module is imported, which imports all primitive modules
            putil
        except NameError:
            import honeybee_radiance.putil as putil
        
        # gather all modifier objects
        modifiers = {}
        for mod in data['modifiers']:
            modifiers[mod['name']] = putil.dict_to_modifier(mod)

        # build each of the sub-sets
        wall_set, floor_set, roof_ceiling_set, aperture_set, door_set, shade_set, \
            air_wall_mod = cls._get_subsets_from_abridged(data, modifiers)

        return cls(data['name'], wall_set, floor_set, roof_ceiling_set,
                   aperture_set, door_set, shade_set, air_wall_mod)

    @classmethod
    def from_dict_abridged(cls, data, modifier_dict):
        """Create a ModifierSet from an abridged dictionary.

        Args:
            data: A ModifierSetAbridged dictionary.
            modifier_dict: A dictionary with modifier names as keys and
                honeybee modifier objects as values. These will be used to
                assign the modifiers to the ModifierSet object.
        """
        assert data['type'] == 'ModifierSetAbridged', \
            'Expected ModifierSetAbridged. Got {}.'.format(data['type'])
        wall_set, floor_set, roof_ceiling_set, aperture_set, door_set, shade_set, \
            air_wall_mod = cls._get_subsets_from_abridged(data, modifier_dict)
        return cls(data['name'], wall_set, floor_set, roof_ceiling_set,
                   aperture_set, door_set, shade_set, air_wall_mod)

    def to_dict(self, abridged=False, none_for_defaults=True):
        """Get ModifierSet as a dictionary.

        Args:
            abridged: Boolean noting whether detailed materials and modifier
                objects should be written into the ModifierSet (False) or just
                an abridged version (True). Default: False.
            none_for_defaults: Boolean to note whether default modifiers in the
                set should be included in detail (False) or should be None (True).
                Default: True.
        """
        base = {'type': 'ModifierSet'} if not abridged \
            else {'type': 'ModifierSetAbridged'}

        base['name'] = self.name
        base['wall_set'] = self.wall_set._to_dict(none_for_defaults)
        base['floor_set'] = self.floor_set._to_dict(none_for_defaults)
        base['roof_ceiling_set'] = self.roof_ceiling_set._to_dict(none_for_defaults)
        base['aperture_set'] = self.aperture_set._to_dict(none_for_defaults)
        base['door_set'] = self.door_set._to_dict(none_for_defaults)
        base['shade_set'] = self.shade_set._to_dict(none_for_defaults)
        if none_for_defaults:
            base['air_wall_modifier'] = self._air_wall_modifier.name if \
                self._air_wall_modifier is not None else None
        else:
            base['air_wall_modifier'] = self.air_wall_modifier.name

        if not abridged:
            modifiers = self.modified_modifiers_unique if none_for_defaults \
                else self.modifiers_unique
            base['modifiers'] = [modifier.to_dict() for modifier in modifiers]

        return base

    def duplicate(self):
        """Get a copy of this ModifierSet."""
        return self.__copy__()

    def lock(self):
        """The lock() method to will also lock the WallSet, FloorSet, etc."""
        self._locked = True
        self._wall_set.lock()
        self._floor_set.lock()
        self._roof_ceiling_set.lock()
        self._aperture_set.lock()
        self._door_set.lock()
        self._shade_set.lock()

    def unlock(self):
        """The unlock() method will also unlock the WallSet, FloorSet, etc."""
        self._locked = False
        self._wall_set.unlock()
        self._floor_set.unlock()
        self._roof_ceiling_set.unlock()
        self._aperture_set.unlock()
        self._door_set.unlock()
        self._shade_set.unlock()

    def _get_modifier_from_set(self, face_type_set, boundary_condition):
        """Get a specific modifier from a face_type_set."""
        if boundary_condition == 'Outdoors':
            return face_type_set.exterior_modifier
        else:
            return face_type_set.interior_modifier
    
    @staticmethod
    def _get_subsets_from_abridged(data, modifiers):
        """Get subset objects from and abirdged dictionary."""
        wall_set = ModifierSet._make_modifier_subset(
            data, WallSet(), 'wall_set', modifiers)
        floor_set = ModifierSet._make_modifier_subset(
            data, FloorSet(), 'floor_set', modifiers)
        roof_ceiling_set = ModifierSet._make_modifier_subset(
            data, RoofCeilingSet(), 'roof_ceiling_set', modifiers)
        shade_set = ModifierSet._make_modifier_subset(
            data, ShadeSet(), 'shade_set', modifiers)
        aperture_set = ModifierSet._make_aperture_subset(
            data, ApertureSet(), modifiers)
        door_set = ModifierSet._make_door_subset(data, DoorSet(), modifiers)
        if 'air_wall_modifier' in data and data['air_wall_modifier'] is not None:
            air_wall_mod = modifiers[data['air_wall_modifier']]
        else:
            air_wall_mod = None
        
        return wall_set, floor_set, roof_ceiling_set, aperture_set, door_set, \
            shade_set, air_wall_mod

    @staticmethod
    def _make_modifier_subset(data, sub_set, sub_set_name, modifiers):
        """Make a WallSet, FloorSet, RoofCeilingSet, or ShadeSet from dictionary."""
        if sub_set_name in data:
            if 'exterior_modifier' in data[sub_set_name] and \
                    data[sub_set_name]['exterior_modifier'] is not None:
                sub_set.exterior_modifier = \
                    modifiers[data[sub_set_name]['exterior_modifier']]
            if 'interior_modifier' in data[sub_set_name] and \
                    data[sub_set_name]['interior_modifier'] is not None:
                sub_set.interior_modifier = \
                    modifiers[data[sub_set_name]['interior_modifier']]
        return sub_set

    @staticmethod
    def _make_aperture_subset(data, sub_set, modifiers):
        """Make an ApertureSet from a dictionary."""
        if 'aperture_set' in data:
            if 'window_modifier' in data['aperture_set'] and \
                    data['aperture_set']['window_modifier'] is not None:
                sub_set.window_modifier = \
                    modifiers[data['aperture_set']['window_modifier']]
            if 'interior_modifier' in data['aperture_set'] and \
                    data['aperture_set']['interior_modifier'] is not None:
                sub_set.interior_modifier = \
                    modifiers[data['aperture_set']['interior_modifier']]
            if 'skylight_modifier' in data['aperture_set'] and \
                    data['aperture_set']['skylight_modifier'] is not None:
                sub_set.skylight_modifier = \
                    modifiers[data['aperture_set']['skylight_modifier']]
            if 'operable_modifier' in data['aperture_set'] and \
                    data['aperture_set']['operable_modifier'] is not None:
                sub_set.operable_modifier = \
                    modifiers[data['aperture_set']['operable_modifier']]
        return sub_set

    @staticmethod
    def _make_door_subset(data, sub_set, modifiers):
        """Make a DoorSet from dictionary."""
        if 'door_set' in data:
            if 'exterior_modifier' in data['door_set'] and \
                    data['door_set']['exterior_modifier'] is not None:
                sub_set.exterior_modifier = \
                    modifiers[data['door_set']['exterior_modifier']]
            if 'interior_modifier' in data['door_set'] and \
                    data['door_set']['interior_modifier'] is not None:
                sub_set.interior_modifier = \
                    modifiers[data['door_set']['interior_modifier']]
            if 'exterior_glass_modifier' in data['door_set'] and \
                    data['door_set']['exterior_glass_modifier'] is not None:
                sub_set.exterior_glass_modifier = \
                    modifiers[data['door_set']['exterior_glass_modifier']]
            if 'interior_glass_modifier' in data['door_set'] and \
                    data['door_set']['interior_glass_modifier'] is not None:
                sub_set.interior_glass_modifier = \
                    modifiers[data['door_set']['interior_glass_modifier']]
            if 'overhead_modifier' in data['door_set'] and \
                    data['door_set']['overhead_modifier'] is not None:
                sub_set.overhead_modifier = \
                    modifiers[data['door_set']['overhead_modifier']]
        return sub_set

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __copy__(self):
        return ModifierSet(
            self.name,
            self.wall_set.duplicate(),
            self.floor_set.duplicate(),
            self.roof_ceiling_set.duplicate(),
            self.aperture_set.duplicate(),
            self.door_set.duplicate(),
            self.shade_set.duplicate(),
            self._air_wall_modifier
        )

    def __key(self):
        """A tuple based on the object properties, useful for hashing."""
        return (self.name,) + tuple(hash(mod) for mod in self.modifiers)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, ModifierSet) and self.__key() == other.__key()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'Radiance Modifier Set: {}'.format(self.name)


@lockable
class _BaseSet(object):
    """Base class for the sets assigned to Faces (WallSet, FloorSet, RoofCeilingSet)."""

    __slots__ = ('_exterior_modifier', '_interior_modifier', '_locked')

    def __init__(self, exterior_modifier=None, interior_modifier=None):
        """Initialize set.

        Args:
            exterior_modifier: A radiance modifier object for faces with an
                Outdoors boundary condition.
            interior_modifier: A radiance modifier object for faces with a boundary
                condition other than Outdoors.
        """
        self._locked = False  # unlocked by default
        self.exterior_modifier = exterior_modifier
        self.interior_modifier = interior_modifier

    @property
    def exterior_modifier(self):
        """Get or set the modifier for exterior objects."""
        if self._exterior_modifier is None:
            return _default_modifiers[self.__class__.__name__]['exterior']
        return self._exterior_modifier

    @exterior_modifier.setter
    def exterior_modifier(self, value):
        self._exterior_modifier = self._validate_modifier(value)

    @property
    def interior_modifier(self):
        """Get or set the modifier for interior objects."""
        if self._interior_modifier is None:
            return _default_modifiers[self.__class__.__name__]['interior']
        return self._interior_modifier

    @interior_modifier.setter
    def interior_modifier(self, value):
        self._interior_modifier = self._validate_modifier(value)

    @property
    def modifiers(self):
        """List of all modifiers contained within the set."""
        return [getattr(self, attr[1:]) for attr in self._slots]

    @property
    def modified_modifiers(self):
        """List of all modifiers that are not defaulted within the set."""
        _modifiers = [getattr(self, attr) for attr in self._slots]
        modifiers = [
            modifier for modifier in _modifiers
            if modifier is not None
        ]
        return modifiers

    @property
    def is_modified(self):
        """Boolean noting whether any modifiers are modified from the default."""
        return len(self.modified_modifiers) != 0

    def _to_dict(self, none_for_defaults=True):
        """Get the ModifierSet as a dictionary.

        Args:
            none_for_defaults: Boolean to note whether default modifiers in the
                set should be included in detail (False) or should be None (True).
                Default: True.
        """
        attributes = self._slots
        if none_for_defaults:
            base = {
                attr[1:]:getattr(self, attr[1:]).name
                if getattr(self, attr) is not None else None
                for attr in attributes
                }
        else:
            base = {
                attr[1:]:getattr(self, attr[1:]).name
                for attr in attributes
            }
        
        base['type'] = self.__class__.__name__ + 'Abridged'
        return base

    def duplicate(self):
        """Get a copy of this set."""
        return self.__copy__()

    def _validate_modifier(self, value):
        """Check a modifier before assigning it."""
        if value is not None:
            assert isinstance(value, Modifier), \
                'Expected modifier. Got {}'.format(type(value))
            value.lock()   # lock editing in case modifier has multiple references
        return value

    @property
    def _slots(self):
        """Return slots including the ones from the baseclass if any."""
        slots = set(self.__slots__)
        for cls in self.__class__.__mro__[:-1]:
            for s in getattr(cls, '__slots__', tuple()):
                if s in slots:
                    continue
                slots.add(s)
        slots.remove('_locked')
        return slots

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __len__(self):
        return 2

    def __iter__(self):
        return iter(self.modifiers)

    def __copy__(self):
        return self.__class__(self._exterior_modifier, self._interior_modifier)

    def __repr__(self):
        name = self.__class__.__name__.split('Set')[0]
        return '{} Modifier Set:\n Exterior: {}\n Interior: {}'.format(
            name, self.exterior_modifier.name, self.interior_modifier.name
        )


@lockable
class WallSet(_BaseSet):
    """Set containing all radiance modifiers needed to for an radiance model's Walls.

    Properties:
        * exterior_modifier
        * interior_modifier
        * modifiers
        * modified_modifiers
        * is_modified
    """
    __slots__ = ()


@lockable
class FloorSet(_BaseSet):
    """Set containing all radiance modifiers needed to for an radiance model's floors.

    Properties:
        * exterior_modifier
        * interior_modifier
        * modifiers
        * modified_modifiers
        * is_modified
    """
    __slots__ = ()


@lockable
class RoofCeilingSet(_BaseSet):
    """Set containing all radiance modifiers needed to for an radiance model's roofs.

    Properties:
        * exterior_modifier
        * interior_modifier
        * modifiers
        * modified_modifiers
        * is_modified
    """
    __slots__ = ()


@lockable
class ShadeSet(_BaseSet):
    """Set containing all radiance modifiers needed to for an radiance model's Shade.

    Properties:
        * exterior_modifier
        * interior_modifier
        * modifiers
        * modified_modifiers
        * is_modified
    """
    __slots__ = ()


@lockable
class ApertureSet(_BaseSet):
    """Set containing all radiance modifiers needed to for a radiance model's Apertures.

    Properties:
        * window_modifier
        * interior_modifier
        * skylight_modifier
        * operable_modifier
        * modifiers
        * modified_modifiers
        * is_modified
    """
    __slots__ = ('_skylight_modifier', '_operable_modifier')

    def __init__(self, window_modifier=None, interior_modifier=None,
                 skylight_modifier=None, operable_modifier=None):
        """Initialize aperture set.

        Args:
            window_modifier: A modifier object for apertures with an Outdoors
                boundary condition, False is_operable property, and Wall parent Face.
            interior_modifier: A modifier object for apertures with a Surface
                boundary condition.
            skylight_modifier: : A modifier object for apertures with an Outdoors
                boundary condition, False is_operable property, and a RoofCeiling
                or Floor face type for their parent face.
            operable_modifier: A modifier object for apertures with an Outdoors
                boundary condition and a True is_operable property.
        """
        _BaseSet.__init__(self, window_modifier, interior_modifier)
        self.skylight_modifier = skylight_modifier
        self.operable_modifier = operable_modifier

    @property
    def window_modifier(self):
        """Get or set the modifier for exterior fixed apertures in walls."""
        if self._exterior_modifier is None:
            return _default_modifiers[self.__class__.__name__]['exterior']
        return self._exterior_modifier

    @window_modifier.setter
    def window_modifier(self, value):
        self._exterior_modifier = self._validate_modifier(value)

    @property
    def operable_modifier(self):
        """Get or set the modifier for operable apertures."""
        if self._operable_modifier is None:
            return _default_modifiers[self.__class__.__name__]['operable']
        return self._operable_modifier

    @operable_modifier.setter
    def operable_modifier(self, value):
        self._operable_modifier = self._validate_modifier(value)

    @property
    def skylight_modifier(self):
        """Get or set the modifier for apertures in roofs."""
        if self._skylight_modifier is None:
            return _default_modifiers[self.__class__.__name__]['skylight']
        return self._skylight_modifier

    @skylight_modifier.setter
    def skylight_modifier(self, value):
        self._skylight_modifier = self._validate_modifier(value)
    
    def _to_dict(self, none_for_defaults=True):
        """Get the ModifierSet as a dictionary.

        Args:
            none_for_defaults: Boolean to note whether default modifiers in the
                set should be included in detail (False) or should be None (True).
                Default: True.
        """
        base = _BaseSet._to_dict(self, none_for_defaults)
        if 'exterior_modifier' in base:
            base['window_modifier'] = base['exterior_modifier']
            del base['exterior_modifier']
        return base

    def __len__(self):
        return 4

    def __copy__(self):
        return self.__class__(
            self._exterior_modifier,
            self._interior_modifier,
            self._skylight_modifier,
            self._operable_modifier
        )

    def __repr__(self):
        return 'Aperture Modifier Set:\n Exterior: {}\n Interior: {}' \
            '\n Skylight: {}\n Operable: {}'.format(
            self.window_modifier.name,
            self.interior_modifier.name,
            self.skylight_modifier.name,
            self.operable_modifier.name
        )


@lockable
class DoorSet(_BaseSet):
    """Set containing all radiance modifiers needed to for an radiance model's Doors.

    Properties:
        * exterior_modifier
        * interior_modifier
        * exterior_glass_modifier
        * interior_glass_modifier
        * overhead_modifier
        * modifiers
        * modified_modifiers
        * is_modified
    """
    __slots__ = ('_overhead_modifier', '_exterior_glass_modifier',
                 '_interior_glass_modifier')

    def __init__(self, exterior_modifier=None, interior_modifier=None,
                 exterior_glass_modifier=None, interior_glass_modifier=None,
                 overhead_modifier=None):
        """Initialize door set.

        Args:
            exterior_modifier: A window modifier object for apertures
                with an Outdoors boundary condition.
            interior_modifier: A window modifier object for apertures
                with a Surface boundary condition.
            exterior_glass_modifier:
            interior_glass_modifier:
            overhead_modifier: : A window modifier object for doors with an
                Outdoors boundary condition and a RoofCeiling or Floor face type for
                their parent face.
        """
        _BaseSet.__init__(self, exterior_modifier, interior_modifier)
        self.exterior_glass_modifier = exterior_glass_modifier
        self.interior_glass_modifier = interior_glass_modifier
        self.overhead_modifier = overhead_modifier

    @property
    def exterior_glass_modifier(self):
        """Get or set the modifier for exterior glass doors."""
        if self._exterior_glass_modifier is None:
            return _default_modifiers[self.__class__.__name__]['exterior_glass']
        return self._exterior_glass_modifier

    @exterior_glass_modifier.setter
    def exterior_glass_modifier(self, value):
        self._exterior_glass_modifier = self._validate_modifier(value)

    @property
    def interior_glass_modifier(self):
        """Get or set the modifier for interior glass doors."""
        if self._interior_glass_modifier is None:
            return _default_modifiers[self.__class__.__name__]['interior_glass']
        return self._interior_glass_modifier

    @interior_glass_modifier.setter
    def interior_glass_modifier(self, value):
        self._interior_glass_modifier = self._validate_modifier(value)

    @property
    def overhead_modifier(self):
        """Get or set the modifier for skylights."""
        if self._overhead_modifier is None:
            return _default_modifiers[self.__class__.__name__]['overhead']
        return self._overhead_modifier

    @overhead_modifier.setter
    def overhead_modifier(self, value):
        self._overhead_modifier = self._validate_modifier(value)

    def __len__(self):
        return 3

    def __copy__(self):
        return self.__class__(
            self._exterior_modifier,
            self._interior_modifier,
            self._exterior_glass_modifier,
            self._interior_glass_modifier,
            self._overhead_modifier
        )

    def __repr__(self):
        return 'Door Modifier Set:\n Exterior: {}\n Interior: {}' \
            '\n Exterior Glass: {}\n Interior Glass: {}\n Overhead: {}'.format(
            self.exterior_modifier.name,
            self.interior_modifier.name,
            self.exterior_glass_modifier.name,
            self.interior_glass_modifier.name,
            self.overhead_modifier.name
        )
