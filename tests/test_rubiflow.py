"""
Unit test suite for RubiFlow framework.
"""

import unittest
from rubiflow import (
    Client,
    Session,
    RubiFlowCrypto,
    User,
    Chat,
    Message,
    RubiFlowError,
    InvalidAuthError,
    ApiError,
)
from rubiflow.exceptions import check_api_status


class TestRubiFlowCrypto(unittest.TestCase):
    def setUp(self):
        self.auth = "abcdefghijklmnopqrstuvwxyz123456"
        self.data = {"hello": "world", "number": 42}

    def test_passphrase_derivation(self):
        passphrase = RubiFlowCrypto.create_secret_passphrase(self.auth)
        self.assertEqual(len(passphrase), 32)
        # Verify deterministic output
        self.assertEqual(passphrase, RubiFlowCrypto.create_secret_passphrase(self.auth))

    def test_aes_round_trip(self):
        encrypted = RubiFlowCrypto.encrypt_aes(self.data, self.auth)
        self.assertIsInstance(encrypted, str)
        decrypted = RubiFlowCrypto.decrypt_aes(encrypted, self.auth)
        self.assertEqual(decrypted, self.data)

    def test_auth_disguise(self):
        disguised = RubiFlowCrypto.disguise_auth(self.auth)
        self.assertEqual(len(disguised), len(self.auth))
        self.assertNotEqual(disguised, self.auth)

    def test_rsa_key_pair_and_sign(self):
        priv_pem, pub_pem = RubiFlowCrypto.generate_rsa_key_pair()
        self.assertIn("BEGIN PRIVATE KEY", priv_pem)
        self.assertIn("BEGIN PUBLIC KEY", pub_pem)

        sample_data = "encrypted_base64_string_test"
        signature = RubiFlowCrypto.sign_rsa_sha256(sample_data, priv_pem)
        self.assertIsInstance(signature, str)
        self.assertTrue(len(signature) > 50)


class TestRubiFlowSession(unittest.TestCase):
    def test_string_session_roundtrip(self):
        priv_pem, _ = RubiFlowCrypto.generate_rsa_key_pair()
        session = Session(
            auth="abcdefghijklmnopqrstuvwxyz123456",
            private_key_pem=priv_pem,
            dc_url="https://messengerg2c332.iranlms.ir",
            user_guid="u0TestGuid",
            phone="989123456789",
        )
        s_str = session.to_string()
        self.assertTrue(s_str.startswith("RubiFlow$"))

        restored = Session.from_string(s_str)
        self.assertEqual(restored.auth, session.auth)
        self.assertEqual(restored.dc_url, session.dc_url)
        self.assertEqual(restored.user_guid, session.user_guid)
        self.assertEqual(restored.phone, session.phone)


class TestRubiFlowModels(unittest.TestCase):
    def test_user_model(self):
        raw = {
            "user_guid": "u0123",
            "first_name": "Ali",
            "last_name": "Rezaei",
            "username": "alirez",
            "phone": "989000000000",
            "bio": "Developer",
        }
        u = User.from_dict(raw)
        self.assertEqual(u.guid, "u0123")
        self.assertEqual(u.full_name, "Ali Rezaei")
        self.assertEqual(u.mention, "@alirez")

    def test_chat_model(self):
        raw = {
            "object_guid": "c0123",
            "type": "Channel",
            "title": "RubiFlow News",
            "last_message_id": "100",
            "count_unseen": 5,
        }
        c = Chat.from_dict(raw)
        self.assertEqual(c.guid, "c0123")
        self.assertTrue(c.is_channel)
        self.assertFalse(c.is_group)
        self.assertEqual(c.unread_count, 5)

    def test_message_model(self):
        raw = {
            "message_id": "555",
            "object_guid": "u0123",
            "author_object_guid": "u0123",
            "text": "Hello RubiFlow",
            "time": 1700000000,
        }
        m = Message.from_dict(raw)
        self.assertEqual(m.message_id, "555")
        self.assertEqual(m.text, "Hello RubiFlow")


class TestRubiFlowExceptions(unittest.TestCase):
    def test_api_status_ok(self):
        # Should not raise
        check_api_status({"status": "OK"})

    def test_invalid_auth_raised(self):
        with self.assertRaises(InvalidAuthError):
            check_api_status({"status": "ERROR_GENERIC", "status_det": "INVALID_AUTH"})

    def test_generic_api_error_raised(self):
        with self.assertRaises(ApiError):
            check_api_status({"status": "ERROR_GENERIC", "status_det": "CUSTOM_ERROR"})


class TestClientMethodsExistence(unittest.TestCase):
    def test_methods_attached_to_client(self):
        """Verifies that all domain methods are properly exposed on Client."""
        app = Client(auth="test" * 8, private_key_pem="test")
        
        # Core
        self.assertTrue(hasattr(app, "execute"))
        self.assertTrue(hasattr(app, "invoke"))
        self.assertTrue(hasattr(app, "on_message"))
        self.assertTrue(hasattr(app, "run"))
        
        # Auth
        self.assertTrue(hasattr(app, "send_code"))
        self.assertTrue(hasattr(app, "sign_in"))
        self.assertTrue(hasattr(app, "logout"))
        self.assertTrue(hasattr(app, "register_device"))
        
        # Messages
        self.assertTrue(hasattr(app, "send_message"))
        self.assertTrue(hasattr(app, "edit_message"))
        self.assertTrue(hasattr(app, "delete_messages"))
        self.assertTrue(hasattr(app, "forward_messages"))
        self.assertTrue(hasattr(app, "get_messages"))
        
        # Chats
        self.assertTrue(hasattr(app, "get_chats"))
        self.assertTrue(hasattr(app, "get_chats_by_id"))
        self.assertTrue(hasattr(app, "seen_chats"))
        
        # Groups & Channels
        self.assertTrue(hasattr(app, "add_group"))
        self.assertTrue(hasattr(app, "create_group_voice_chat"))
        self.assertTrue(hasattr(app, "add_channel"))
        self.assertTrue(hasattr(app, "create_join_link"))
        
        # Users & Files & Folders & Settings
        self.assertTrue(hasattr(app, "get_me"))
        self.assertTrue(hasattr(app, "upload_file"))
        self.assertTrue(hasattr(app, "add_folder"))
        self.assertTrue(hasattr(app, "get_privacy_setting"))
        
        # Rubino & VOD & Wallet
        self.assertTrue(hasattr(app, "get_rubino_explore"))
        self.assertTrue(hasattr(app, "like_post"))
        self.assertTrue(hasattr(app, "get_vod_media"))
        self.assertTrue(hasattr(app, "get_wallet_status"))


if __name__ == "__main__":
    unittest.main()
