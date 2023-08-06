"""
Message connection adapter tests.
"""

from gaphor import UML
from gaphor.diagram.interactions.lifeline import LifelineItem
from gaphor.diagram.interactions.message import MessageItem
from gaphor.tests import TestCase


class BasicMessageConnectionsTestCase(TestCase):
    def test_head_glue(self):
        """Test message head glue
        """
        ll = self.create(LifelineItem)
        msg = self.create(MessageItem)

        # get head port
        port = ll.ports()[0]
        glued = self.allow(msg, msg.head, ll, port)
        assert glued

    def test_invisible_lifetime_glue(self):
        """Test message to invisible lifetime glue
        """
        ll = self.create(LifelineItem)
        msg = self.create(MessageItem)

        glued = self.allow(msg, msg.head, ll, ll.lifetime.port)

        assert not ll.lifetime.visible
        assert not glued

    def test_visible_lifetime_glue(self):
        """Test message to visible lifetime glue
        """
        ll = self.create(LifelineItem)
        msg = self.create(MessageItem)

        ll.lifetime.visible = True

        glued = self.allow(msg, msg.head, ll, ll.lifetime.port)
        assert glued

    def test_lost_message_connection(self):
        """Test lost message connection
        """
        ll = self.create(LifelineItem)
        msg = self.create(MessageItem)

        self.connect(msg, msg.head, ll)

        # If one side is connected a "lost" message is created
        self.assertTrue(msg.subject is not None)
        assert msg.subject.messageKind == "lost"

        messages = self.kindof(UML.Message)
        occurrences = self.kindof(UML.MessageOccurrenceSpecification)

        assert 1 == len(messages)
        assert 1 == len(occurrences)
        assert messages[0] is msg.subject
        assert occurrences[0] is msg.subject.sendEvent

    def test_found_message_connection(self):
        """Test found message connection
        """
        ll = self.create(LifelineItem)
        msg = self.create(MessageItem)

        self.connect(msg, msg.tail, ll)

        # If one side is connected a "found" message is created
        self.assertTrue(msg.subject is not None)
        assert msg.subject.messageKind == "found"

        messages = self.kindof(UML.Message)
        occurrences = self.kindof(UML.MessageOccurrenceSpecification)

        assert 1 == len(messages)
        assert 1 == len(occurrences)
        assert messages[0] is msg.subject
        assert occurrences[0] is msg.subject.receiveEvent

    def test_complete_message_connection(self):
        """Test complete message connection
        """
        ll1 = self.create(LifelineItem)
        ll2 = self.create(LifelineItem)
        msg = self.create(MessageItem)

        self.connect(msg, msg.head, ll1)
        self.connect(msg, msg.tail, ll2)

        # two sides are connected - "complete" message is created
        self.assertTrue(msg.subject is not None)
        assert msg.subject.messageKind == "complete"

        messages = self.kindof(UML.Message)
        occurences = self.kindof(UML.MessageOccurrenceSpecification)

        assert 1 == len(messages)
        assert 2 == len(occurences)
        assert messages[0] is msg.subject
        assert msg.subject.sendEvent in occurences, f"{occurences}"
        assert msg.subject.receiveEvent in occurences, f"{occurences}"

    def test_lifetime_connection(self):
        """Test messages' lifetimes connection
        """
        msg = self.create(MessageItem)
        ll1 = self.create(LifelineItem)
        ll2 = self.create(LifelineItem)

        # make lifelines to be in sequence diagram mode
        ll1.lifetime.visible = True
        ll2.lifetime.visible = True
        assert ll1.lifetime.visible and ll2.lifetime.visible

        # connect lifetimes with messages message to lifeline's head
        self.connect(msg, msg.head, ll1, ll1.lifetime.port)
        self.connect(msg, msg.tail, ll2, ll2.lifetime.port)

        assert msg.subject is not None
        assert msg.subject.messageKind == "complete"

    def test_disconnection(self):
        """Test message disconnection
        """
        ll1 = self.create(LifelineItem)
        ll2 = self.create(LifelineItem)
        msg = self.create(MessageItem)

        self.connect(msg, msg.head, ll1)
        self.connect(msg, msg.tail, ll2)

        # one side disconnection
        self.disconnect(msg, msg.head)
        assert msg.subject is not None, f"{msg.subject}"

        # 2nd side disconnection
        self.disconnect(msg, msg.tail)
        assert msg.subject is None, f"{msg.subject}"

    def test_lifetime_connectivity_on_head(self):
        """Test lifeline's lifetime connectivity change on head connection
        """
        ll = self.create(LifelineItem)
        msg = self.create(MessageItem)

        # connect message to lifeline's head, lifeline's lifetime
        # visibility and connectivity should change
        self.connect(msg, msg.head, ll)
        assert not ll.lifetime.visible
        assert not ll.lifetime.connectable
        assert ll.lifetime.MIN_LENGTH == ll.lifetime.min_length

        # ... and disconnection
        self.disconnect(msg, msg.head)
        assert ll.lifetime.connectable
        assert ll.lifetime.MIN_LENGTH == ll.lifetime.min_length

    def test_lifetime_connectivity_on_lifetime(self):
        """Test lifeline's lifetime connectivity change on lifetime connection
        """
        ll = self.create(LifelineItem)
        msg = self.create(MessageItem)

        ll.lifetime.visible = True

        # connect message to lifeline's lifetime, lifeline's lifetime
        # visibility and connectivity should be unchanged
        self.connect(msg, msg.head, ll, ll.lifetime.port)
        assert ll.lifetime.connectable
        assert ll.lifetime.MIN_LENGTH_VISIBLE == ll.lifetime.min_length

        # ... and disconnection
        self.disconnect(msg, msg.head)
        assert ll.lifetime.connectable
        assert ll.lifetime.visible
        assert ll.lifetime.MIN_LENGTH == ll.lifetime.min_length


class DiagramModeMessageConnectionTestCase(TestCase):
    def test_message_glue_cd(self):
        """Test gluing message on communication diagram."""

        lifeline1 = self.create(LifelineItem)
        lifeline2 = self.create(LifelineItem)
        message = self.create(MessageItem)

        # make second lifeline to be in sequence diagram mode
        lifeline2.lifetime.visible = True

        # connect head of message to lifeline's head
        self.connect(message, message.head, lifeline1)

        glued = self.allow(message, message.tail, lifeline2, lifeline2.lifetime.port)
        # no connection possible as 2nd lifeline is in sequence diagram
        # mode
        self.assertFalse(glued)

    def test_message_glue_sd(self):
        """Test gluing message on sequence diagram."""

        msg = self.create(MessageItem)
        ll1 = self.create(LifelineItem)
        ll2 = self.create(LifelineItem)

        # 1st lifeline - communication diagram
        # 2nd lifeline - sequence diagram
        ll2.lifetime.visible = True

        # connect lifetime of message to lifeline's lifetime
        self.connect(msg, msg.head, ll1, ll1.lifetime.port)

        glued = self.allow(msg, msg.tail, ll2)
        # no connection possible as 2nd lifeline is in communication
        # diagram mode
        self.assertFalse(glued)

    def test_messages_disconnect_cd(self):
        """Test disconnecting messages on communication diagram
        """
        ll1 = self.create(LifelineItem)
        ll2 = self.create(LifelineItem)
        msg = self.create(MessageItem)

        self.connect(msg, msg.head, ll1)
        self.connect(msg, msg.tail, ll2)

        subject = msg.subject

        assert subject.sendEvent and subject.receiveEvent

        messages = list(self.kindof(UML.Message))
        occurrences = set(self.kindof(UML.MessageOccurrenceSpecification))

        # verify integrity of messages
        self.assertEqual(1, len(messages))
        assert 2 == len(occurrences)
