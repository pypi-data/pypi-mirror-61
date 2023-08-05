from canoser import Struct, Uint8, Uint64
from libra.event import EventHandle
from libra.account_config import AccountConfig
from io import StringIO


class AccountState(Struct):
    _fields = [
        ('ordered_map', {})
    ]

    def get_resource(self):
        resource = self.ordered_map[AccountConfig.account_resource_path()]
        if resource:
            return AccountResource.deserialize(resource)
        else:
            return None

    def to_json_serializable(self):
        amap = super().to_json_serializable()
        ar = self.get_resource()
        if ar:
            amap["account_resource_path"] = AccountConfig.account_resource_path().hex()
            amap["decoded_account_resource"] = ar.to_json_serializable()
        return amap


class AccountResource(Struct):
    """
    A Rust/Python representation of an Account resource.
    This is not how the Account is represented in the VM but it's a convenient representation.
    """
    _fields = [
        ('authentication_key', bytes),
        ('balance', Uint64),
        ('delegated_key_rotation_capability', bool),
        ('delegated_withdrawal_capability', bool),
        ('received_events', EventHandle),
        ('sent_events', EventHandle),
        ('sequence_number', Uint64),
        ('event_generator', Uint64)
    ]

    @classmethod
    def get_account_resource_or_default(cls, blob):
        if blob:
            omap = AccountState.deserialize(blob.blob).ordered_map
            resource = omap[AccountConfig.account_resource_path()]
            return cls.deserialize(resource)
        else:
            return cls()

    def get_event_handle_by_query_path(self, query_path):
        if AccountConfig.account_received_event_path() == query_path:
            return self.received_events
        elif AccountConfig.account_sent_event_path() == query_path:
            return self.sent_events
        else:
            libra.proof.bail("Unrecognized query path: {}", query_path);
