import importlib.util
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('claims',ROOT/'scripts/check_site_claims.py')
MODULE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
class LifecycleTests(unittest.TestCase):
    def test_current_site(self):
        self.assertEqual([],MODULE.validate(ROOT))
    def test_regressions(self):
        cases=[('index.html','<a href="/nownest/">NowNest</a>','deprecated product'),
               ('apps/index.html','<p>Mews &amp; Woofs</p>','deprecated product'),
               ('portfolio/index.html','<p>Rung</p>','deprecated product'),
               ('sitemap.xml','https://edoworks.com/rung/','sitemap'),
               ('index.html','<a href="/missing/">Missing</a>','local link')]
        for filename,addition,expected in cases:
            with self.subTest(filename=filename,addition=addition),TemporaryDirectory() as d:
                root=Path(d)/'site'
                shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
                p=root/filename;p.write_text(p.read_text()+addition)
                self.assertTrue(any(expected in e for e in MODULE.validate(root)))
    def test_notice_required(self):
        with TemporaryDirectory() as d:
            root=Path(d)/'site'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
            p=root/'nownest/index.html';p.write_text(p.read_text().replace('noindex','index'))
            self.assertTrue(any('retirement disclosure' in e for e in MODULE.validate(root)))
