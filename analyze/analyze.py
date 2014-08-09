from nltk import FreqDist
from nltk.tokenize.punkt import PunktWordTokenizer
from feed.models import Story, Feed

class RSSFeed:
    def __init__(self, passed_string):
        try:
            self.passed_string = passed_string
            self.tokenized_string = self.tokenize_string(self.passed_string)
            self.frequency_distribution = self.get_frequency_dist(
                self.tokenized_string)
        except Exception as err:
            print err
            return None

    # Turn raw strings to word tokens usable by nltk
    def tokenize_string(self, passed_string):
        if len(passed_string) > 0:
            return (PunktWordTokenizer().tokenize(passed_string))

    # Acquire a frequency distribution of tokens
    def get_frequency_dist(self, tokenized_string):
        return FreqDist(tokenized_string)

    def find_common_usage(self, length_at_least, times_word_used):
        return sorted(word for word in set(self.tokenized_string)
                      if len(word) >= length_at_least and
                      self.frequency_distribution[word] >= times_word_used)

    def simple_test_print(self, name, length=4, times_used=3):
        print str(name)
        for word in self.find_common_usage(length, times_used):
            print word
        print ("\n\n")


test_string = RSSFeed('(CNN) -- The United States is considering air strikes in Iraq in response to a militant surge in northern areas that has left minority groups trapped by fighting, a U.S. official told CNN.The official said the possibility of such military action "has been something" the Obama administration "has been talking about for some time and the latest news just might meet the threshold for action."Iraq\'s largest Christian town has been overrun by the same militant Islamists who have gained a foothold in parts of eastern Syria and western and northern Iraq. Christians targeted in key Iraqi towns UN: Kids dying from poor living situation The advance by ISIS, or the Islamic State, has caused thousands of Christians in the city to flee, just as other minority groups targeted by it have done. ISIS seeks to create an Islamic caliphate that stretches from Syria to Iraq. It has aggressively targeted Iraqi minority religious groups. The Obama administration is talking with officials in Baghdad and Erbil and is looking at options to provide humanitarian support, including but not limited to Iraqi government air drops, another U.S. official said. White House spokesman Josh Earnest refused to offer any details on possible actions under consideration. Asked specifically about possible air strikes, he said he was not in position to comment on that. Noting Iraq has many problems, he described the current situation as "a particularly acute one" with "innocent populations persecuted just because of their ethnic identity," calling it "disturbing." At the same time, Earnest repeated principles for any possible military involvement in Iraq previously stated by President Barack Obama, declaring no American military solution existed for Iraq and no U.S. ground troops would be sent there. "We can\'t solve these problems for them. These problems can only be solved with Iraqi political solutions," he said. A senior State Department official said the United States also is weighing opening a humanitarian corridor, providing support to Kurdish and Iraqi forces. The United States has 245 military personnel in Iraq, 90 of whom are advisers. The carrier USS George H.W. Bush is also in the region as well as other Navy ships.')  # noqa
test_string_deux = RSSFeed('The U.S. aircraft carrier George H.W. Bush and her more than 50 attack aircraft were available to conduct airstrikes against Islamic militants in Iraq if President Obama gives the order, Pentagon officials said Friday.The Bush and her accompanying battle group of ships "were in the region and ready for any tasking," said Rear Adm. John Kirby, the Pentagon press secretary. Kirby would not confirm several reports that the Bush had already moved into the Persian Gulf.The 1092-foot, nuclear-powered carrier, named for former President George H.W. Bush, deployed from her homeport in Norfolk, Va., in February on a regular rotation to the Mediterranean and the Persian Gulf region.The Bush would be among several military options that were being drawn up by Defense Secretary Chuck Hagel and his planning staff for President Obama\'s consideration to stop the swift advance of fighters from the Islamic State of Iraq who have taken over major cities west and north of Baghdad."It\'s our job to provide the Commander-In-Chief with options. We\'re doing that," Kirby said. In addition, the U.S. has also stepped up intelligence surveillance and reconnaissance (ISR) operations with drones over Iraq at the request of the embattled government of Prime Minister Nouri al-Maliki.Kirby said the military options being prepared for Obama were "designed to break the momentum of ISIS forces" which reportedly have come within 50 miles of Baghdad against little resistance from the U.S.-trained Iraqi security forces. Earlier, President Obama said military action of some type by the U.S. was likely in the coming days but he ruled out boots on the ground. Following morning meetings at the White House with Gen. Martin Dempsey, chairman of the Joint Chiefs of Staff, Obama said U.S. action was necessary to stop the ISIS that "could pose a threat eventually to American interests as well." "We will not be sending U.S. troops back into combat in Iraq, but I have asked my national security team to prepare a range of other options that could help support Iraqi security forces, and I\'ll be reviewing those options in the days ahead," Obama said before leaving for a visit to the Standing Rock Sioux Tribal Nation in North Dakota. Obama used the term "ISIL," or Islamic State of Iraq and the Levant, to refer to the ISIS jihadists who have been vastly outnumbered by the Iraqi army and yet have taken over Mosul, a town of two million, by attacking in pickup trucks with small arms. "Look, the United States has poured a lot of money into these Iraqi security forces, and we devoted a lot of training to Iraqi security forces," Obama said. "The fact that they are not willing to stand and fight, and defend their posts against admittedly hardened terrorists, but not terrorists who are overwhelming in numbers, indicates that there\'s a problem with morale," Obama said. Obama repeated his charged that the Shia-dominated Iraqi government has failed to heal rifts with the Sunni communities in western Iraq who have given support to ISIS. "Unfortunately, Iraq\'s leaders have been unable to overcome too often the mistrust and sectarian differences that have long been simmering there, and that\'s created vulnerabilities within the Iraqi government as well as their security forces," Obama said. At the Pentagon, Kirby said there were no immediate plans to withdraw the approximately 9,000 U.S. defense and civilian personnel in Iraq beyond several hundred contractors who were working on a project in Balad north of Baghdad. Kirby said the employer of the contractors was making arrangements for them to leave the country. Kirby and other officials said they could not confirm ISIS claims on Twitter that as many as 1,700 captured Shia Iraqi soldiers have been executed. However, Navi Pillay, the United Nations High Commissioner for Human Rights, expressed "extreme alarm" at the claim and said he had seen verified reports of "summary executions and extra-judicial killings.')  # noqa

test_string.simple_test_print('cnn')
test_string_deux.simple_test_print('fox')


#Stop Words
#Adding stop words from nltk stop words