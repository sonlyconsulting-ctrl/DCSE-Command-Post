from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]


class WorkflowSurfaceTests(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / "apps/escd/web/index.html").read_text()
        self.workflow_html = (ROOT / "apps/escd/web/workflows.html").read_text()
        self.workflow_handler = (ROOT / "apps/escd/api/workflow_index.py").read_text()
        self.workflow_api = (ROOT / "apps/escd/runtime/workflow_api.py").read_text()
        self.entrypoint = (ROOT / "api/escd.py").read_text()
        self.vercel = (ROOT / "vercel.json").read_text()

    def test_operator_workflow_ui_is_not_backend_only(self):
        for required in [
            'id="workflowList"','id="workflowDetail"','id="workflowTemplate"',
            'id="workflowContextType"','id="workflowContextRef"','id="workflowBindings"',
            'id="workflowSourceRefs"','id="workflowJobId"','id="instantiateWorkflow"',
            'Template','Version','Execution','Steps','Approval:','Evidence:','Attempts:','Next permitted step:',
        ]:
            self.assertIn(required, self.html)
        self.assertIn('@media(max-width:600px)', self.html)
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn('prefers-reduced-motion', self.html)

    def test_dedicated_operator_view_exercises_workflow_lifecycle(self):
        for required in [
            'ESCD Workflows','Start workflow','Resume workflow','Retry workflow','Complete workflow',
            'Mark ready','Run step','Run with approved decision','Ready for retry','Complete','Fail',
            'workflow_step:','evidence reference','execution_authorized','Governed job',
        ]:
            self.assertIn(required, self.workflow_html)
        for route in ['/workflows','/workflows/detail?instance_id=','/workflows/transition','/workflows/steps/transition']:
            self.assertIn(route, self.workflow_html)
        self.assertIn('@media(max-width:520px)', self.workflow_html)
        self.assertIn('prefers-reduced-motion', self.workflow_html)
        self.assertIn('aria-live="polite"', self.workflow_html)

    def test_ui_calls_governed_workflow_routes(self):
        for route in ['/workflow-templates','/workflows','/workflows/detail?instance_id=','/workflows/instantiate']:
            self.assertIn(route, self.html)

    def test_authenticated_handler_layers_workflow_routes_over_existing_runtime(self):
        self.assertIn('class handler(BaseESCDHandler)', self.workflow_handler)
        self.assertIn('self._authorized()', self.workflow_handler)
        self.assertIn('dispatch_get(repo, self.path)', self.workflow_handler)
        self.assertIn('dispatch_post(repo, path, payload)', self.workflow_handler)
        self.assertNotIn('SUPABASE_SERVICE_ROLE_KEY', self.workflow_handler)

    def test_workflow_api_has_required_operator_contracts(self):
        for route in [
            '/api/escd/workflow-templates','/api/escd/workflows','/api/escd/workflows/detail',
            '/api/escd/workflows/instantiate','/api/escd/workflows/transition','/api/escd/workflows/steps/transition',
        ]:
            self.assertIn(route, self.workflow_api)
        self.assertIn('runtime_template_promotion_prohibited', self.workflow_api)
        self.assertIn('workflow_execution_not_authorized', self.workflow_api)
        self.assertIn('workflow_step_prohibited', self.workflow_api)

    def test_candidate_entrypoint_and_rewrites_are_specific_before_generic(self):
        self.assertIn('WorkflowESCDHandler', self.entrypoint)
        self.assertIn('escd_path', self.entrypoint)
        specific = self.vercel.index('/api/escd/(.*)')
        generic = self.vercel.index('/api/(.*)')
        self.assertLess(specific, generic)
        self.assertIn('/api/escd?escd_path=$1', self.vercel)
        self.assertIn('/escd/workflows', self.vercel)
        self.assertIn('/apps/escd/web/workflows.html', self.vercel)
        self.assertIn('/apps/escd/web/index.html', self.vercel)

    def test_no_ddna_or_employment_scope_was_bundled_into_workflow_surface(self):
        combined = (self.workflow_api + self.workflow_handler + self.entrypoint + self.html + self.workflow_html).lower()
        self.assertNotIn('ddna_runtime_mode', combined)
        self.assertNotIn('dcs_employment', combined)


if __name__ == "__main__":
    unittest.main()
