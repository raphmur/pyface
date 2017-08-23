from __future__ import absolute_import

import platform

from traits.testing.unittest_tools import unittest

from ..constant import CANCEL, NO, OK, YES
from ..toolkit import toolkit_object
from ..window import Window


is_qt = toolkit_object.toolkit == 'qt4'
if is_qt:
    from pyface.qt import qt_api

GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')

ModalDialogTester = toolkit_object('util.modal_dialog_tester:ModalDialogTester')
no_modal_dialog_tester = (ModalDialogTester.__name__ == 'Unimplemented')

is_pyqt5 = (is_qt and qt_api == 'pyqt5')
is_pyqt4_linux = (is_qt and qt_api == 'pyqt' and platform.system() == 'Linux')


@unittest.skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestWindow(unittest.TestCase, GuiTestAssistant):

    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.window = Window()

    def tearDown(self):
        if self.window.control is not None:
            with self.delete_widget(self.window.control):
                self.window.destroy()
        self.window = None
        GuiTestAssistant.tearDown(self)

    def test_destroy(self):
        # test that destroy works even when no control
        self.window.destroy()
        self.gui.process_events()

    def test_open_close(self):
        # test that opening and closing works as expected
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                self.window.open()
        self.gui.process_events()
        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                self.window.close()
        self.gui.process_events()

    def test_show(self):
        # test that showing works as expected
        self.window._create()
        self.window.show(True)
        self.gui.process_events()
        self.window.show(False)
        self.gui.process_events()
        self.window.destroy()
        self.gui.process_events()

    def test_activate(self):
        # test that activation works as expected
        self.window.open()
        self.gui.process_events()
        self.window.activate()
        self.gui.process_events()
        self.window.close()
        self.gui.process_events()

    def test_position(self):
        # test that default position works as expected
        self.window.position = (100, 100)
        self.window.open()
        self.gui.process_events()
        self.window.close()
        self.gui.process_events()

    def test_reposition(self):
        # test that changing position works as expected
        self.window.open()
        self.gui.process_events()
        self.window.position = (100, 100)
        self.gui.process_events()
        self.window.close()
        self.gui.process_events()

    def test_size(self):
        # test that default size works as expected
        self.window.size = (100, 100)
        self.window.open()
        self.gui.process_events()
        self.window.close()
        self.gui.process_events()

    def test_resize(self):
        # test that changing size works as expected
        self.window.open()
        self.gui.process_events()
        self.window.size = (100, 100)
        self.gui.process_events()
        self.window.close()
        self.gui.process_events()

    def test_title(self):
        # test that default title works as expected
        self.window.title = "Test Title"
        self.window.open()
        self.gui.process_events()
        self.window.close()
        self.gui.process_events()

    def test_retitle(self):
        # test that changing title works as expected
        self.window.open()
        self.gui.process_events()
        self.window.title = "Test Title"
        self.gui.process_events()
        self.window.close()
        self.gui.process_events()

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_confirm_reject(self):
        # test that cancel works as expected
        tester = ModalDialogTester(
            lambda: self.window.confirm("message", cancel=True))
        tester.open_and_run(when_opened=lambda x: x.close(accept=False))
        self.assertEqual(tester.result, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    @unittest.skipIf(is_pyqt5, "Confirmation dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Confirmation dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    def test_confirm_yes(self):
        # test that yes works as expected
        tester = ModalDialogTester(lambda: self.window.confirm("message"))
        tester.open_and_wait(when_opened=lambda x: x.click_button(YES))
        self.gui.process_events()
        self.assertEqual(tester.result, YES)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    @unittest.skipIf(is_pyqt5, "Confirmation dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Confirmation dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    def test_confirm_no(self):
        # test that no works as expected
        tester = ModalDialogTester(lambda: self.window.confirm("message"))
        tester.open_and_wait(when_opened=lambda x: x.click_button(NO))
        self.gui.process_events()
        self.assertEqual(tester.result, NO)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    @unittest.skipIf(is_pyqt5, "Confirmation dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Confirmation dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    def test_confirm_cancel(self):
        # test that cncel works as expected
        tester = ModalDialogTester(
            lambda: self.window.confirm("message", cancel=True))
        tester.open_and_wait(when_opened=lambda x: x.click_button(CANCEL))
        self.gui.process_events()
        self.assertEqual(tester.result, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_information_accept(self):
        self._check_message_dialog_accept(self.window.information)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    @unittest.skipIf(is_pyqt5, "Message dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Message dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    def test_information_ok(self):
        self._check_message_dialog_ok(self.window.information)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_warning_accept(self):
        self._check_message_dialog_accept(self.window.warning)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    @unittest.skipIf(is_pyqt5, "Message dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Message dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    def test_warning_ok(self):
        self._check_message_dialog_ok(self.window.warning)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_error_accept(self):
        self._check_message_dialog_accept(self.window.error)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    @unittest.skipIf(is_pyqt5, "Message dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Message dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    def test_error_ok(self):
        self._check_message_dialog_ok(self.window.error)

    def _check_message_dialog_ok(self, method):
        tester = self._setup_tester(method)
        tester.open_and_wait(when_opened=lambda x: x.click_button(OK))
        self.assertIsNone(tester.result)

    def _check_message_dialog_accept(self, method):
        tester = self._setup_tester(method)
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        self.assertIsNone(tester.result)

    def _setup_tester(self, method):
        kwargs = {
            'title': 'Title',
            'detail': 'Detail',
            'informative': 'Informative'
        }
        tester = ModalDialogTester(lambda: method("message", **kwargs))
        return tester
