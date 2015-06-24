# An acceptance test for signatrix.

import unittest
from io import StringIO

from line import Line
from work import Work


litora = ' Litora, multum ille et terris iactatus et alto '

early_aeneid = StringIO("""

Arma virumque cano, Troiae qui primus ab oris 
Italiam, fato profugus, Laviniaque venit 
litora, multum ille et terris iactatus et alto 
vi superum saevae memorem Iunonis ob iram; 
multa quoque et bello passus, dum conderet urbem,    5 
inferretque deos Latio, genus unde Latinum, 
Albanique patres, atque altae moenia Romae.
Musa, mihi causas memora, quo numine laeso, 
quidve dolens, regina deum tot volvere casus 
insignem pietate virum, tot adire labores    10 
impulerit. Tantaene animis caelestibus irae?

Urbs antiqua fuit, Tyrii tenuere coloni, 

""")

class AcceptanceTest(unittest.TestCase):

    maxDiff = None

    def test_litora(self):
        line = Line(litora)
        self.assertCountEqual(
            [str(scan) for scan in line.scans],
            [
"lī'-tŏ-ră / mul-t(um)⁀il-/-l(e)⁀et te'r-/-ris jac-/-tā'-tŭ-s⁀ĕ-/-t⁀a'l-to"
            ]
        )

    def test_early_aeneid(self):
        work = Work(early_aeneid, name='Aeneid 1')
        self.assertCountEqual(
            work.scans_strings(),
            [
"a'r-mă vĭ-/-ru'm-quĕ că'-/-nō trō-/-jā'-ĕ quĭ / prī'-mŭ-s⁀ă-/-b⁀ō'-ris",
"a'r-mă vĭ-/-ru'm-quĕ că'-/-nō trŏ'-jă-/-ē quī / prī'-mŭ-s⁀ă-/-b⁀ō'-ris",
"a'r-mă vĭ-/-ru'm-quē / cā'-nŏ trŏ-/-jā'-ĕ quĭ / prī'-mŭ-s⁀ă-/-b⁀ō'-ris",
"a'r-mă vĭ-/-ru'm-quĕ că'-/-nō trŏ'-ĭ-/-æ quī / prī'-mŭ-s⁀ă-/-b⁀ō'-ris",
"a'r-mă vĭ-/-ru'm-quĕ că'-/-nō trō'-/-jæ quī / prī'-mŭ-s⁀ă-/-b⁀ō'-ris",
"a'r-mă vĭ-/-ru'm-quĕ că'-/-nō trŏ-ĭ-/-ā'-ĕ quĭ / prī'-mŭ-s⁀ă-/-b⁀ō'-ris",
"a'r-mă vĭ-/-ru'm-quē / cā'-nŏ trŏ'-/-jæ quī / prī'-mŭ-s⁀ă-/-b⁀ō'-ris",
"",
"ī-ta'l-/-jam fā'-/-tō prō-/-fū'-gŭ-s⁀lă-/-vi'n-jă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fă'-tŏ / prō'-fŭ-gŭ-/-s⁀lā-ŭ-ĭ-/-nī'-ă-quĕ / vē'-nit",
"ī-ta'l-/-jam fă'-tŏ / prō'-fŭ-gŭ-/-s⁀lā-ū-/-i'n-jă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fā'-/-tō prŏ'-fŭ-/-gus lă-vĭ-/-nī'-ă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fă'-tŏ / prō'-fŭ-gŭ-/-s⁀lā-ū-/-i'n-jă-quĕ / vē'-nit",
"ī-ta'l-/-jam fă'-tŏ / prō-fū'-/-gus lă-ŭ-/-i'n-jă-quĕ / vē'-nit",
"ī-ta'l-/-jam fā'-/-tō prŏ'-fŭ-/-gus lā-/-vi'n-jă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fā'-/-tō prŏ'-fŭ-/-gū-s⁀lă-vĭ-/-nī'-ă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fă'-tŏ / prō-fū'-/-gus lau-/-i'n-jă-quĕ / vē'-nit",
"ī-ta'l-/-jam fā'-/-tō prŏ'-fŭ-/-gus lă-ŭ-/-i'n-jă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fā'-/-tō prŏ'-fŭ-/-gus lă-ŭ-/-i'n-jă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fă'-tŏ / prō'-fŭ-gŭ-/-s⁀lā-vī-/-nī'-ă-quĕ / vē'-nit",
"ī-ta'l-/-jam fā'-/-tō prŏ'-fŭ-/-gū-s⁀lă-vĭ-/-nī'-ă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fā'-/-tō prŏ'-fŭ-/-gus lau-/-i'n-jă-quĕ / vē'-nit",
"ī-ta'l-/-jam fă'-tŏ / prō-fū'-/-gū-s⁀lă-ŭ-/-i'n-jă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fă'-tŏ / prō-fū'-/-gus lā-/-vi'n-jă-quĕ / vē'-nit",
"ī-ta'l-/-jam fă'-tŏ / prō-fū'-/-gū-s⁀lā-/-vi'n-jă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fā'-/-tō prŏ'-fŭ-/-gū-s⁀lă-ŭ-/-i'n-jă-quĕ / vē'-nit",
"ī-ta'l-/-jam fā'-/-tō prŏ'-fŭ-/-gus lau-/-i'n-jă-quĕ / vē'-nit",
"ī-ta'l-/-jam fā'-/-tō prŏ'-fŭ-/-gū-s⁀lă-ŭ-/-i'n-jă-quĕ / vē'-nit",
"ī-ta'l-/-jam fă'-tŏ / prō-fū'-/-gus lā-/-vi'n-jă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fā'-/-tō prŏ'-fŭ-/-gus lā-/-vi'n-jă-quĕ / vē'-nit",
"ī-ta'l-/-jam fă'-tŏ / prō'-fŭ-gŭ-/-s⁀lā-ŭ-ĭ-/-nī'-ă-quĕ / vē'-nit",
"ī-ta'l-/-jam fă'-tŏ / prō-fū'-/-gū-s⁀lă-vĭ-/-nī'-ă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fă'-tŏ / prō-fū'-/-gū-s⁀lau-/-i'n-jă-quĕ / vē'-nit",
"ī-tā-/-lī'-am / fā'-tŏ prŏ-/-fū'-gŭ-s⁀lă-/-vi'n-jă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fă'-tŏ / prō-fū'-/-gū-s⁀lă-ŭ-/-i'n-jă-quĕ / vē'-nit",
"ī-ta'l-/-jam fā'-/-tō prŏ'-fŭ-/-gū-s⁀lau-/-i'n-jă-quĕ / vē'-nit",
"ī-ta'l-/-jam fā'-/-tō prŏ'-fŭ-/-gū-s⁀lā-/-vi'n-jă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fă'-tŏ / prō-fū'-/-gū-s⁀lă-vĭ-/-nī'-ă-quĕ / vē'-nit",
"ī-ta'l-/-jam fă'-tŏ / prō'-fŭ-gŭ-/-s⁀lā-vī-/-nī'-ă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fā'-/-tō prō-/-fū'-gŭ-s⁀lă-/-vi'n-jă-quĕ / vē'-nit",
"ī-ta'l-/-jam fă'-tŏ / prō-fū'-/-gus lă-vĭ-/-nī'-ă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fă'-tŏ / prō'-fŭ-gŭ-/-s⁀lau-ī-/-nī'-ă-quĕ / vē'-nit",
"ī-ta'l-/-jam fă'-tŏ / prō-fū'-/-gus lau-/-i'n-jă-quĕ / vē'-nit",
"ī-ta'l-/-jam fā'-/-tō prŏ'-fŭ-/-gus lă-vĭ-/-nī'-ă-quĕ / vē'-nit",
"ī-ta'l-/-jam fă'-tŏ / prō'-fŭ-gŭ-/-s⁀lau-ī-/-nī'-ă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fă'-tŏ / prō-fū'-/-gū-s⁀lā-/-vi'n-jă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fā'-/-tō prŏ'-fŭ-/-gū-s⁀lā-/-vi'n-jă-quĕ / vē'-nit",
"ī-ta'l-/-jam fă'-tŏ / prō-fū'-/-gū-s⁀lau-/-i'n-jă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fă'-tŏ / prō-fū'-/-gus lă-ŭ-/-i'n-jă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fā'-/-tō prŏ'-fŭ-/-gū-s⁀lau-/-i'n-jă-quĕ / vē'-nit",
"ī-tă'-lĭ-/-am fă'-tŏ / prō-fū'-/-gus lă-vĭ-/-nī'-ă-quĕ / vē'-nit",
"",
"lī'-tŏ-ră / mul-t(um)⁀il-/-l(e)⁀et te'r-/-ris jac-/-tā'-tŭ-s⁀ĕ-/-t⁀a'l-to",
"",
"vī sŭ'-pĕ-/-rum să'-ĕ-/-væ mē'-/-mō-r(em)⁀ĭ-ŭ-/-nō'-nĭ-s⁀ŏ-/-b⁀ī'-ram",
"vī sŭ'-pĕ-/-rum să'-ĕ-/-væ mĕ'-mŏ-/-r(em)⁀ī-ū-/-nō'-nĭ-s⁀ŏ-/-b⁀ī'-ram",
"vī sŭ'-pĕ-/-rum sæ'-/-væ mĕ'-mŏ-/-rē-m⁀ĭ-ŭ-/-nō'-nĭ-s⁀ŏ-/-b⁀ī'-ram",
"vī sŭ'-pĕ-/-rum să'-ĕ-/-væ mĕ'-mŏ-/-rem jū-/-nō'-nĭ-s⁀ŏ-/-b⁀ī'-ram",
"vī sŭ'-pĕ-/-rum să-ĕ-/-vā'-ĕ mĕ'-/-mō-r(em)⁀ĭ-ŭ-/-nō'-nĭ-s⁀ŏ-/-b⁀ī'-ram",
"vī sŭ'-pĕ-/-rum sæ'-/-væ mĕ'-mŏ-/-rem jū-/-nō'-nĭ-s⁀ŏ-/-b⁀ī'-ram",
"vī sŭ'-pĕ-/-rum sæ'-/-væ mē'-/-mō-r(em)⁀ĭ-ŭ-/-nō'-nĭ-s⁀ŏ-/-b⁀ī'-ram",
"vī sŭ'-pĕ-/-rum sæ'-/-væ mĕ'-mŏ-/-r(em)⁀ī-ū-/-nō'-nĭ-s⁀ŏ-/-b⁀ī'-ram",
"vī sŭ'-pĕ-/-rum să'-ĕ-/-væ mĕ'-mŏ-/-rē-m⁀ĭ-ŭ-/-nō'-nĭ-s⁀ŏ-/-b⁀ī'-ram",
"vī sŭ'-pĕ-/-rum sæ-/-vā'-ĕ mĕ'-/-mō-r(em)⁀ĭ-ŭ-/-nō'-nĭ-s⁀ŏ-/-b⁀ī'-ram",
"",
"mu'l-tă quŏ-/-qu(e)⁀et be'l-/-lō pa's-/-sus dum / co'n-dĕ-rĕ-/-t⁀u'r-bem",
"",
"in-fer-/-re't-quĕ dĕ'-/-ō-s⁀lă'-tĭ-/-ō gĕ'-nŭ-/-s⁀u'n-dĕ lă-/-tī'-num",
"in-fer-/-re't-quĕ dĕ'-/-ō-s⁀la't-/-jō gĕ'-nŭ-/-s⁀u'n-dĕ lă-/-tī'-num",
"in-fer-/-re't-quĕ dĕ'-/-os lă'-tĭ-/-ō gĕ'-nŭ-/-s⁀u'n-dĕ lă-/-tī'-num",
"in-fer-/-re't-quĕ dĕ'-/-os la't-/-jō gĕ'-nŭ-/-s⁀u'n-dĕ lă-/-tī'-num",
"",
"al-bă'-nĭ-/-quē pā'-/-trē-s⁀at-/-qu(e)⁀a'l-tæ / mœ'-nĭ-ă / rō'-mæ",
"al-bă'-nĭ-/-quē pă'-trĕ-/-s⁀at-qu(e)⁀al-/-tā'-ĕ mŏ-/-e'n-jă rŏ-/-mā'-e",
"al-bă'-nĭ-/-quē pă'-trĕ-/-s⁀a't-quē / a'l-tă-ĕ / mœ'n-jă rŏ-/-mā'-e",
"al-bă'-nĭ-/-quē pă'-trĕ-/-s⁀at-qu(e)⁀a'l-/-tæ mō-/-ē'-nĭ-ă / rō'-mæ",
"al-bă'-nĭ-/-quē pă'-trĕ-/-s⁀at-qu(e)⁀a'l-/-tæ mŏ-ĕ-/-nī'-ă rŏ-/-mā'-e",
"al-bă'-nĭ-/-quē pă'-trĕ-/-s⁀at-qu(e)⁀al-/-tā'-ĕ mŏ-/-ē'-nĭ-ă / rō'-mæ",
"al-bā-/-nī'-quĕ pă'-/-trē-s⁀at-/-qu(e)⁀a'l-tæ / mœ'-nĭ-ă / rō'-mæ",
"al-bă'-nĭ-/-quē pă'-trĕ-/-s⁀at-qu(e)⁀a'l-/-tæ mō-/-e'n-jă rŏ-/-mā'-e",
"al-bă'-nĭ-/-quē pā'-/-trē-s⁀at-/-qu(e)⁀a'l-tă-ĕ / mœ'-nĭ-ă / rō'-mæ",
"al-bā-/-nī'-quĕ pă'-/-trē-s⁀at-/-qu(e)⁀a'l-tă-ĕ / mœ'n-jă rŏ-/-mā'-e",
"al-bă'-nĭ-/-quē pa't-/-rē-s⁀at-/-qu(e)⁀a'l-tă-ĕ / mœ'n-jă rŏ-/-mā'-e",
"al-bă'-nĭ-/-quē pa't-/-rē-s⁀at-/-qu(e)⁀a'l-tă-ĕ / mœ'-nĭ-ă / rō'-mæ",
"al-bă'-nĭ-/-quē pă'-trĕ-/-s⁀a't-quē / a'l-tă-ĕ / mœ'-nĭ-ă / rō'-mæ",
"al-bă'-nĭ-/-quē pă'-trĕ-/-s⁀at-qu(e)⁀al-/-tā'-ē / mœ'n-jă rŏ-/-mā'-e",
"al-bā-/-nī'-quĕ pă'-/-trē-s⁀at-/-qu(e)⁀a'l-tă-ĕ / mœ'-nĭ-ă / rō'-mæ",
"al-bă'-nĭ-/-quē pā'-/-trē-s⁀at-/-qu(e)⁀a'l-tă-ĕ / mœ'n-jă rŏ-/-mā'-e",
"al-bă'-nĭ-/-quē pa't-/-rē-s⁀at-/-qu(e)⁀a'l-tæ / mœ'-nĭ-ă / rō'-mæ",
"al-bă'-nĭ-/-quē pa't-/-rē-s⁀at-/-qu(e)⁀a'l-tæ / mœ'n-jă rŏ-/-mā'-e",
"al-bă'-nĭ-/-quē pă'-trĕ-/-s⁀a't-quē / a'l-tæ / mœ'n-jă rŏ-/-mā'-e",
"al-bă'-nĭ-/-quē pā'-/-trē-s⁀at-/-qu(e)⁀a'l-tæ / mœ'n-jă rŏ-/-mā'-e",
"al-bă'-nĭ-/-quē pă'-trĕ-/-s⁀at-qu(e)⁀a'l-/-tæ mœ-/-nī'-ă rŏ-/-mā'-e",
"al-bă'-nĭ-/-quē pă'-trĕ-/-s⁀at-qu(e)⁀al-/-tā'-ē / mœ'-nĭ-ă / rō'-mæ",
"al-bā-/-nī'-quĕ pă'-/-trē-s⁀at-/-qu(e)⁀a'l-tæ / mœ'n-jă rŏ-/-mā'-e",
"al-bă'-nĭ-/-quē pă'-trĕ-/-s⁀a't-quē / a'l-tæ / mœ'-nĭ-ă / rō'-mæ",
"",
"mū'-să mĭ'-/-hī că'-ŭ-/-sas mĕ'-mŏ-/-rā quō / nū'-mĭ-nĕ / læ'-so",
"mū'-să mĭ'-/-hī cau'-/-sas mĕ'-mŏ-/-rā quō / nū'-mĭ-nĕ / læ'-so",
"mū'-să mĭ'-/-hī că'-ŭ-/-sas mĕ'-mŏ-/-rā quŏ nŭ-/-mī'-nĕ lă-/-ē'-so",
"mū'-să mĭ'-/-hī cau'-/-sas mĕ'-mŏ-/-rā quŏ nŭ-/-mī'-nĕ lă-/-ē'-so",
"mū'-să mĭ'-/-hī cau'-/-sas mē-/-mō'-ră quŏ / nū'-mĭ-nĕ / læ'-so",
"mū'-să mĭ'-/-hī că'-ŭ-/-sas mē-/-mō'-ră quŏ / nū'-mĭ-nĕ / læ'-so",
"",
"qui'd-vĕ dŏ'-/-lens rĕ'-gĭ-/-nā dē'-/-um tot / vo'l-vĕ-rĕ / cā'-sus",
"qui'd-vĕ dŏ'-/-lens rē-/-gī'-nă dĕ'-/-um tot / vo'l-vĕ-rĕ / cā'-sus",
"quī'-dŭ-ĕ / dō'-lens / rē'-gĭ-nă / deum tot / vo'l-vĕ-rĕ / cā'-sus",
"qui'd-vĕ dŏ'-/-lens rē-/-gī'-nā / deum tot / vo'l-vĕ-rĕ / cā'-sus",
"qui'd-vĕ dŏ'-/-lens rĕ'-gĭ-/-nā deum / tot vō-/-lū'-ĕ-rĕ / cā'-sus",
"qui'd-vē / dō'-lens / rē'-gĭ-nă / deum tot / vo'l-vĕ-rĕ / cā'-sus",
"",
"in-si'g-/-nem pjĕ'-tă-/-tē vī'-/-rum tŏ-t⁀ă-/-dī'-rĕ lă-/-bō'-res",
"in-si'g-/-nem pĭ-ĕ-/-tā'-tĕ vĭ'-/-rum tŏ-t⁀ă-/-dī'-rĕ lă-/-bō'-res",
"in-si'g-/-nem pjē-/-tā'-tĕ vĭ'-/-rum tŏ-t⁀ă-/-dī'-rĕ lă-/-bō'-res",
"",
"im-pŭ'-lĕ-/-rit ta'n-/-tæ-n(e)⁀ă'-nĭ-/-mis că-ĕ-/-le's-tĭ-bŭ-/-s⁀ī'-ræ",
"im-pŭ'-lĕ-/-rit ta'n-/-tæ-n(e)⁀ă'-nĭ-/-mī-s⁀cæ-/-le's-tĭ-bŭ-/-s⁀ī'-ræ",
"im-pŭ'-lĕ-/-rit ta'n-/-tæ-n(e)⁀ă'-nĭ-/-mī-s⁀că-ĕ-/-lē'-stĭ-bŭ-/-s⁀ī'-ræ",
"im-pŭ'-lĕ-/-rit ta'n-/-tæ-n(e)⁀ă'-nĭ-/-mī-s⁀că-ĕ-/-le's-tĭ-bŭ-/-s⁀ī'-ræ",
"im-pŭ'-lĕ-/-rit ta'n-/-tæ-n(e)⁀ă'-nĭ-/-mis cæ-/-lē'-stĭ-bŭ-/-s⁀ī'-ræ",
"im-pŭ'-lĕ-/-rit ta'n-/-tæ-n(e)⁀ă'-nĭ-/-mī-s⁀cæ-/-lē'-stĭ-bŭ-/-s⁀ī'-ræ",
"im-pŭ'-lĕ-/-rit ta'n-/-tæ-n(e)⁀ă'-nĭ-/-mis că-ĕ-/-lē'-stĭ-bŭ-/-s⁀ī'-ræ",
"im-pŭ'-lĕ-/-rit ta'n-/-tæ-n(e)⁀ă'-nĭ-/-mis cæ-/-le's-tĭ-bŭ-/-s⁀ī'-ræ",
"",
"urb-s⁀an-/-tī'-quă fŭ'-/-it ty'-rĭ-/-ī tĕ-nŭ-/-ē'-rĕ cŏ-/-lō'-ni",
"urb-s⁀an-/-tī'-quā / fvit ty'-rĭ-/-ī ten-/-vē'-rĕ cŏ-/-lō'-ni",
"urb-s⁀an-/-tī'-quā / fvit ty'r-/-jī ten-/-vē'-rĕ cŏ-/-lō'-ni",
"urb-s⁀an-/-tī'-quā / fvit ty'r-/-jī tĕ-nŭ-/-ē'-rĕ cŏ-/-lō'-ni",
"urb-s⁀an-/-tī'-quă fŭ'-/-it ty'r-/-jī ten-/-vē'-rĕ cŏ-/-lō'-ni",
"urb-s⁀an-/-tī'-quă fŭ'-/-it ty'r-/-jī tĕ-nŭ-/-ē'-rĕ cŏ-/-lō'-ni",
"urb-s⁀an-/-tī'-quă fŭ'-/-it ty'-rĭ-/-ī ten-/-vē'-rĕ cŏ-/-lō'-ni",
"urb-s⁀an-/-tī'-quā / fvit ty'-rĭ-/-ī tĕ-nŭ-/-ē'-rĕ cŏ-/-lō'-ni",
""
            ]
        )


if __name__ == '__main__':
    #import cProfile
    #cProfile.run('unittest.main()')
    unittest.main()
