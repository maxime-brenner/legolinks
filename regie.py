

class Webgain():

    def __init__(self, campaign, program):
        self.campaign=campaign
        self.program=program
        self.link="https://track.webgains.com/click.html?wgcampaignid={0}&wgprogramid={1}&wgtarget={2}"

    def create_aff_link(self, url):
        aff_link=self.link.format(self.campaign, self.program, url)

        print(aff_link)

        return aff_link
