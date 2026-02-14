import veip_sdk


def test_sdk_spec_binding_does_not_raise():
    veip_sdk.assert_spec_binding()
