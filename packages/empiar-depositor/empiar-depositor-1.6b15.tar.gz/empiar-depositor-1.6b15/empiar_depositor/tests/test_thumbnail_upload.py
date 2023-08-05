import unittest
from empiar_depositor.empiar_depositor import EmpiarDepositor
from mock import Mock, patch
from requests.models import Response
from empiar_depositor.tests.testutils import capture, EmpiarDepositorTest


class TestThumbnailUpload(EmpiarDepositorTest):
    @patch('empiar_depositor.empiar_depositor.requests.post')
    def test_no_response(self, mock_post):
        mock_post.return_value = None

        emp_dep = EmpiarDepositor("ABC123", self.json_path, "",
                                  entry_thumbnail=self.thumbnail_path)

        c = emp_dep.thumbnail_upload()
        self.assertEqual(c, 1)

    @patch('empiar_depositor.empiar_depositor.requests.post')
    def test_no_permission_stdout(self, mock_post):
        mock_post.return_value = Mock(ok=True, spec=Response)
        mock_post.return_value.status_code = 403
        mock_post.return_value.json.return_value = {'detail': 'You do not have permission to perform this action.'}

        emp_dep = EmpiarDepositor("ABC123", self.json_path, "",
                                  entry_thumbnail=self.thumbnail_path)
  
        with capture(emp_dep.thumbnail_upload) as output:
            self.assertTrue('The upload of the thumbnail for EMPIAR deposition was not successful. Returned response:'
                            in output and 'Status code: 403' in output)

    @patch('empiar_depositor.empiar_depositor.requests.post')
    def test_no_permission_return(self, mock_post):
        mock_post.return_value = Mock(ok=True, spec=Response)
        mock_post.return_value.status_code = 403
        mock_post.return_value.json.return_value = {'detail': 'You do not have permission to perform this action.'}

        emp_dep = EmpiarDepositor("ABC123", self.json_path, "",
                                  entry_thumbnail=self.thumbnail_path)

        c = emp_dep.thumbnail_upload()
        self.assertEqual(c, 1)

    @patch('empiar_depositor.empiar_depositor.requests.post')
    def test_successful_upload(self, mock_post):
        mock_post.return_value = Mock(ok=True, spec=Response)
        mock_post.return_value.json.return_value = {'thumbnail_upload': True}

        emp_dep = EmpiarDepositor("ABC123", self.json_path, "",
                                  entry_thumbnail=self.thumbnail_path)
  
        c = emp_dep.thumbnail_upload()
        self.assertEqual(c, 0)


if __name__ == '__main__':
    unittest.main()
