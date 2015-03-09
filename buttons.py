from pandac.PandaModules import *
loadPrcFile('config/config_dev.prc')

from direct.actor.Actor import Actor
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.gui.DirectGui import *
from direct.directutil import Mopath
from direct.actor.Actor import Actor
from direct.gui.DirectGui import DirectButton
from toontown.election.DistributedInvasionSuit import DistributedInvasionSuit
from toontown.suit import DistributedSuitBase, SuitDNA, BossCog
from direct.directbase import DirectStart
from direct.directbase import DirectStart
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from funnyfarm.toonbase import FunnyFarmGlobals
from toontown.toon import NPCToons
from toontown.toon import Toon
import __builtin__
import sys, os

FunnyFarmGlobals.setNametagGlobals()
FunnyFarmGlobals.setParticleManagers()

class game:
	name = 'toontown'
	process = 'client'

base.game = game()
__builtin__.game = base.game

class MovieMaker():    
    
    def __init__(self):
        self.movieButtons()
        self.cogs = []
        self.playgrounds = []
        self.toons = []
        
    def oobeCamera(self):
        base.oobe()
        render.find('**/camera').hide()

    """Lets Start Off With Playgrounds"""
    def ttcPlayground(self):
        ttcplayground = loader.loadModel('phase_15/hood/toontown_central.bam')
        ttcplayground.reparentTo(render)
        ttcplayground.find('**/hill').setTransparency(TransparencyAttrib.MBinary, 1)
        ttcsky = loader.loadModel('phase_3.5/models/props/TT_sky.bam')
        ttcsky.reparentTo(render)
        self.playgrounds.append(ttcplayground)
        self.playgrounds.append(ttcsky)

    def ddPlayground(self):
        self.ddplayground = loader.loadModel('phase_15/hood/donalds_dock.bam')
        self.ddplayground.reparentTo(render)
        boat = self.ddplayground.find('**/donalds_boat')
        boat.unstash()
        self.eastWestMopath = Mopath.Mopath()
        self.westEastMopath = Mopath.Mopath()
        self.eastWestMopath.loadFile('phase_6/paths/dd-e-w.bam')
        self.eastWestMopathInterval = MopathInterval(self.eastWestMopath, boat)
        ewBoatTrack = ParallelEndTogether(Parallel(self.eastWestMopathInterval, name='ew-boat'))
        self.westEastMopath.loadFile('phase_6/paths/dd-w-e.bam')
        self.westEastMopathInterval = MopathInterval(self.westEastMopath, boat)
        weBoatTrack = ParallelEndTogether(Parallel(self.westEastMopathInterval, name='we-boat'))
        PIER_TIME = 5.0
        eastPier = self.ddplayground.find('**/east_pier')
        ePierHpr = VBase3(90, -44.2601, 0)
        ePierTargetHpr = VBase3(90, 0.25, 0)
        westPier = self.ddplayground.find('**/west_pier')
        wPierHpr = VBase3(-90, -44.2601, 0)
        wPierTargetHpr = VBase3(-90, 0.25, 0)
        ePierDownTrack = Parallel(LerpHprInterval(eastPier, PIER_TIME, ePierHpr, ePierTargetHpr), name='e-pier-down')
        ePierUpTrack = Parallel(LerpHprInterval(eastPier, PIER_TIME, ePierTargetHpr, ePierHpr), name='e-pier-up')
        wPierDownTrack = Parallel(LerpHprInterval(westPier, PIER_TIME, wPierHpr, wPierTargetHpr), name='w-pier-down')
        wPierUpTrack = Parallel(LerpHprInterval(westPier, PIER_TIME, wPierTargetHpr, wPierHpr), name='w-pier-up')
        self.ewTrack = ParallelEndTogether(Parallel(ewBoatTrack, ePierDownTrack), wPierUpTrack, name='ew-track')
        self.weTrack = ParallelEndTogether(Parallel(weBoatTrack, wPierDownTrack), ePierUpTrack, name='we-track')
        self.ewTrack.start()
        self.ddsky = loader.loadModel('phase_3.5/models/props/BR_sky.bam')
        self.ddsky.reparentTo(render)
        self.playgrounds.append(self.ddplayground)
        self.playgrounds.append(self.ddsky)

    def dgPlayground(self):
        dgplayground = loader.loadModel('phase_15/hood/daisys_garden.bam')
        dgplayground.reparentTo(render)
        dgsky = loader.loadModel('phase_3.5/models/props/TT_sky.bam')
        dgsky.reparentTo(render)
        self.playgrounds.append(dgplayground)
        self.playgrounds.append(dgsky)

    def mmPlayground(self):
        mmplayground = loader.loadModel('phase_15/hood/minnies_melody_land.bam')
        mmplayground.reparentTo(render)
        mmsky = loader.loadModel('phase_6/models/props/MM_sky.bam')
        mmsky.reparentTo(render)
        self.playgrounds.append(mmplayground)
        self.playgrounds.append(mmsky)

    def brPlayground(self):
        brplayground = loader.loadModel('phase_15/hood/the_burrrgh.bam')
        brplayground.reparentTo(render)
        brsky = loader.loadModel('phase_3.5/models/props/BR_sky.bam')
        brsky.reparentTo(render)
        self.playgrounds.append(brplayground)
        self.playgrounds.append(brsky)

    def ddlPlayground(self):
        ddlplayground = loader.loadModel('phase_15/hood/donalds_dreamland.bam')
        ddlplayground.reparentTo(render)
        ddlsky = loader.loadModel('phase_8/models/props/DL_sky.bam')
        ddlsky.reparentTo(render)
        self.playgrounds.append(ddlplayground)
        self.playgrounds.append(ddlsky)

    def sbPlayground(self):
        sbplayground = loader.loadModel('phase_15/hood/sellbot_hq.bam')
        sbplayground.reparentTo(render)
        self.playgrounds.append(sbplayground)

    def sbfacPlayground(self):
        sbfacplayground = loader.loadModel('phase_15/hood/sellbot_hq_factory.bam')
        sbfacplayground.reparentTo(render)
        self.playgrounds.append(sbfacplayground)

    def cbPlayground(self):
        cbplayground = loader.loadModel('phase_15/hood/cashbot_hq.bam')
        cbplayground.reparentTo(render)
        self.playgrounds.append(cbplayground)

    def lbPlayground(self):
        lbplayground = loader.loadModel('phase_15/hood/lawbot_hq.bam')
        lbplayground.reparentTo(render)
        self.playgrounds.append(lbplayground)

    def bbPlayground(self):
        bbplayground = loader.loadModel('phase_15/hood/bossbot_hq.bam')
        bbplayground.reparentTo(render)
        self.playgrounds.append(bbplayground)

    def killPlayground(self):
        for playground in self.playgrounds:
            playground.removeNode()
        self.playgrounds = []

    """Time For Cogs"""

    def randomCog(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuitRandom()
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        self.cogs.append(suit)

    """Sellbots"""
    def cogHollywood(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('mh')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Mr. Hollywood\nSellbot')
        self.cogs.append(suit)

    def cogMingler(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('m')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Mingler\nSellbot')
        self.cogs.append(suit)

    def cogFace(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('tf')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Two Face\nSellbot')
        self.cogs.append(suit)

    def cogShaker(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('ms')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Mover & Shaker\nSellbot')
        self.cogs.append(suit)

    def cogGlad(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('gh')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Glad Hander\nSellbot')
        self.cogs.append(suit)

    def cogDropper(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('nd')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Name Dropper\nSellbot')
        self.cogs.append(suit)

    def cogTelemarketer(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('tm')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Telemarketer\nSellbot')
        self.cogs.append(suit)

    def cogCold(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('cc')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Cold Caller\nSellbot')
        self.cogs.append(suit)

    """Time For Cashbots"""

    def cogRobber(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('rb')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Robber Baron\nCashbot')
        self.cogs.append(suit)

    def cogShark(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('ls')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Loan Shark\nCashbot')
        self.cogs.append(suit)

    def cogMoney(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('mb')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Moneybags\nCashbot')
        self.cogs.append(suit)

    def cogNumber(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('nc')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Number Cruncher\nCashbot')
        self.cogs.append(suit)

    def cogBean(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('bc')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Bean Counter\nCashbot')
        self.cogs.append(suit)

    def cogTight(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('tw')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Tightwad\nCashbot')
        self.cogs.append(suit)

    def cogPenny(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('pp')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Penny Pincher\nCashbot')
        self.cogs.append(suit)

    def cogShort(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('sc')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Short Change\nCashbot')
        self.cogs.append(suit)

    """Time for Lawbots"""

    def cogWig(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('bw')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Big Wig\nLawbot')
        self.cogs.append(suit)

    def cogEagle(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('le')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Legal Eagle\nLawbot')
        self.cogs.append(suit)

    def cogDoctor(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('sd')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Spin Doctor\nLawbot')
        self.cogs.append(suit)

    def cogStabber(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('bs')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Backstabber\nLawbot')
        self.cogs.append(suit)

    def cogTalker(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('dt')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Double Talker\nLawbot')
        self.cogs.append(suit)

    def cogBlood(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('b')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Bloodsucker\nLawbot')
        self.cogs.append(suit)

    def cogFeeder(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('bf')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Bottom Feeder\nLawbot')
        self.cogs.append(suit)

    def cogCheese(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('tbc')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('The Big Cheese\nBossbot')
        self.cogs.append(suit)

    def cogRaider(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('cr')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Corporate Raider\nBossbot')
        self.cogs.append(suit)

    def cogHunter(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('hh')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Head Hunter\nBossbot')
        self.cogs.append(suit)

    def cogDownsizer(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('ds')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Downsizer\nBossbot')
        self.cogs.append(suit)

    def cogMicro(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('mm')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Micromanager\nBossbot')
        self.cogs.append(suit)

    def cogYesman(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('ym')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Yesman\nBossbot')
        self.cogs.append(suit)

    def cogPencil(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('p')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Pencil Pusher\nBossbot')
        self.cogs.append(suit)

    def cogFlunky(self):
        suit = DistributedInvasionSuit(None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('f')
        suit.setDNA(suitDNA)
        suit.setPos(base.localAvatar.getPos())
        suit.setHpr(base.localAvatar.getHpr())
        suit.loop('neutral')
        suit.reparentTo(render)
        suit.setDisplayName('Flunky\nBossbot')
        self.cogs.append(suit)

    def killCogs(self):
        for cog in self.cogs:
            cog.delete()
        self.cogs = []

    """Time for Cog Animations"""

    def toonFlippy(self):
        toon = NPCToons.createLocalNPC(20001)
        toon.useLOD(1000)
        toon.find('**/250').removeNode()
        toon.find('**/500').removeNode()
        toon.setPos(base.localAvatar.getPos())
        toon.setHpr(base.localAvatar.getHpr())
        toon.initializeBodyCollisions('toon')
        toon.addActive()
        toon.startBlink()
        toon.loop('neutral')
        toon.reparentTo(render)
        self.toons.append(toon)

    def toonDim(self):
        toon = NPCToons.createLocalNPC(2018)
        toon.useLOD(1000)
        toon.find('**/250').removeNode()
        toon.find('**/500').removeNode()
        toon.setPos(base.localAvatar.getPos())
        toon.setHpr(base.localAvatar.getHpr())
        toon.initializeBodyCollisions('toon')
        toon.addActive()
        toon.startBlink()
        toon.loop('neutral')
        toon.reparentTo(render)
        self.toons.append(toon)

    def toonSurlee(self):
        toon = NPCToons.createLocalNPC(2019)
        toon.useLOD(1000)
        toon.find('**/250').removeNode()
        toon.find('**/500').removeNode()
        toon.setPos(base.localAvatar.getPos())
        toon.setHpr(base.localAvatar.getHpr())
        toon.initializeBodyCollisions('toon')
        toon.addActive()
        toon.startBlink()
        toon.loop('neutral')
        toon.reparentTo(render)
        self.toons.append(toon)

    def toonSlappy(self):
        toon = NPCToons.createLocalNPC(2021)
        toon.useLOD(1000)
        toon.find('**/250').removeNode()
        toon.find('**/500').removeNode()
        toon.setPos(base.localAvatar.getPos())
        toon.setHpr(base.localAvatar.getHpr())
        toon.initializeBodyCollisions('toon')
        toon.addActive()
        toon.startBlink()
        toon.loop('neutral')
        toon.reparentTo(render)
        self.toons.append(toon)

    def toonAlec(self):
        toon = NPCToons.createLocalNPC(2022)
        toon.useLOD(1000)
        toon.find('**/250').removeNode()
        toon.find('**/500').removeNode()
        toon.setPos(base.localAvatar.getPos())
        toon.setHpr(base.localAvatar.getHpr())
        toon.initializeBodyCollisions('toon')
        toon.addActive()
        toon.startBlink()
        toon.loop('neutral')
        toon.reparentTo(render)
        self.toons.append(toon)

    def toonPrep(self):
        toon = NPCToons.createLocalNPC(2020)
        toon.useLOD(1000)
        toon.find('**/250').removeNode()
        toon.find('**/500').removeNode()
        toon.setPos(base.localAvatar.getPos())
        toon.setHpr(base.localAvatar.getHpr())
        toon.initializeBodyCollisions('toon')
        toon.addActive()
        toon.startBlink()
        toon.loop('neutral')
        toon.reparentTo(render)
        self.toons.append(toon)

    def toonDaffy(self):
        toon = NPCToons.createLocalNPC(2132)
        toon.useLOD(1000)
        toon.find('**/250').removeNode()
        toon.find('**/500').removeNode()
        toon.setPos(base.localAvatar.getPos())
        toon.setHpr(base.localAvatar.getHpr())
        toon.initializeBodyCollisions('toon')
        toon.addActive()
        toon.startBlink()
        toon.loop('neutral')
        toon.reparentTo(render)
        self.toons.append(toon)

    def toonChuckle(self):
        toon = NPCToons.createLocalNPC(2121)
        toon.useLOD(1000)
        toon.find('**/250').removeNode()
        toon.find('**/500').removeNode()
        toon.setPos(base.localAvatar.getPos())
        toon.setHpr(base.localAvatar.getHpr())
        toon.initializeBodyCollisions('toon')
        toon.addActive()
        toon.startBlink()
        toon.loop('neutral')
        toon.reparentTo(render)
        self.toons.append(toon)

    def toonClara(self):
        toon = NPCToons.createLocalNPC(2011)
        toon.useLOD(1000)
        toon.find('**/250').removeNode()
        toon.find('**/500').removeNode()
        toon.setPos(base.localAvatar.getPos())
        toon.setHpr(base.localAvatar.getHpr())
        toon.initializeBodyCollisions('toon')
        toon.addActive()
        toon.startBlink()
        toon.loop('neutral')
        toon.reparentTo(render)
        self.toons.append(toon)

    def toonPenny(self):
        toon = NPCToons.createLocalNPC(3007)
        toon.useLOD(1000)
        toon.find('**/250').removeNode()
        toon.find('**/500').removeNode()
        toon.setPos(base.localAvatar.getPos())
        toon.setHpr(base.localAvatar.getHpr())
        toon.initializeBodyCollisions('toon')
        toon.addActive()
        toon.startBlink()
        toon.loop('neutral')
        toon.reparentTo(render)
        self.toons.append(toon)

    def toonWill(self):
        toon = NPCToons.createLocalNPC(1001)
        toon.useLOD(1000)
        toon.find('**/250').removeNode()
        toon.find('**/500').removeNode()
        toon.setPos(base.localAvatar.getPos())
        toon.setHpr(base.localAvatar.getHpr())
        toon.initializeBodyCollisions('toon')
        toon.addActive()
        toon.startBlink()
        toon.loop('neutral')
        toon.reparentTo(render)
        self.toons.append(toon)

    def toonOldman(self):
        toon = NPCToons.createLocalNPC(3112)
        toon.useLOD(1000)
        toon.find('**/250').removeNode()
        toon.find('**/500').removeNode()
        toon.setPos(base.localAvatar.getPos())
        toon.setHpr(base.localAvatar.getHpr())
        toon.initializeBodyCollisions('toon')
        toon.addActive()
        toon.startBlink()
        toon.loop('neutral')
        toon.reparentTo(render)
        self.toons.append(toon)
        """End off at oldman"""

    def killToons(self):
        for toon in self.toons:
            toon.delete()
        self.toons = []

    """Time for accessories"""

    def addAccessories(self):
        for toon in self.toons:
            rHand1 = toon.find('**/def_joint_right_hold')
            sillyReader = loader.loadModel('phase_4/models/props/tt_m_prp_acs_sillyReader')
            placeholder1 = rHand1.attachNewNode('SillyReader')
            sillyReader.instanceTo(placeholder1)
            placeholder1.setH(180)
            placeholder1.setScale(render, 1.0)
            placeholder1.setPos(0, 0, 0.1)
        self.toons = []

    """Time for animations for toons"""

    def animationThrow(self):
        for toon in self.toons:
            toon.loop('throw')
        self.toons = []

    def animationWalk(self):
        for toon in self.toons:
            toon.loop('walk')
        self.toons = []

    def animationRun(self):
        for toon in self.toons:
            toon.loop('run')
        self.toons = []

    def animationTeleport(self):
        for toon in self.toons:
            toon.loop('teleport')
        self.toons = []

    def animationBook(self):
        for toon in self.toons:
            toon.loop('book')
        self.toons = []

    def animationJump(self):
        for toon in self.toons:
            toon.loop('jump')
        self.toons = []

    def animationRunningJump(self):
        for toon in self.toons:
            toon.loop('running-jump')
        self.toons = []

    def animationJumpSquat(self):
        for toon in self.toons:
            toon.loop('jump-squat')
        self.toons = []

    def animationPushButton(self):
        for toon in self.toons:
            toon.loop('pushbutton')
        self.toons = []

    def hideButtons(self):
        self.ImgBtn1.hide()
        self.ImgBtn2.hide()
        return 'Buttons Now Hid'
    
    def movieButtons(self):
        #Unlocks
        ButtonImage = loader.loadModel("phase_3/models/gui/quit_button.bam")
        self.ImgBtn1 = DirectButton(frameSize=None, text='Unlocks', image=(ButtonImage.find('**/QuitBtn_UP'), \
        ButtonImage.find('**/QuitBtn_DN'), ButtonImage.find('**/QuitBtn_RLVR')), relief=None, command=self.animationPushButton, text_pos=(0, -0.015), \
        geom=None, pad=(0.01, 0.01), suppressKeys=0, pos = (-1.70,-0,.31), text_scale=0.059, borderWidth=(0.015, 0.01), scale=.7)

        ButtonImage = loader.loadModel("phase_3/models/gui/quit_button.bam")
        self.ImgBtn2 = DirectButton(frameSize=None, text='Wipe', image=(ButtonImage.find('**/QuitBtn_UP'), \
        ButtonImage.find('**/QuitBtn_DN'), ButtonImage.find('**/QuitBtn_RLVR')), relief=None, command=self.brPlayground, text_pos=(0, -0.015), \
        geom=None, pad=(0.01, 0.01), suppressKeys=0, pos = (-1.70,-0,.22), text_scale=0.059, borderWidth=(0.015, 0.01), scale=.7)
        
        ButtonImage = loader.loadModel("phase_3/models/gui/quit_button.bam")
        self.ImgBtn5 = DirectButton(frameSize=None, text='Global Teleport', image=(ButtonImage.find('**/QuitBtn_UP'), \
        ButtonImage.find('**/QuitBtn_DN'), ButtonImage.find('**/QuitBtn_RLVR')), relief=None, command=self.toonOldman, text_pos=(0, -0.015), \
        geom=None, pad=(0.01, 0.01), suppressKeys=0, pos = (-1.70,-0,.12), text_scale=0.059, borderWidth=(0.015, 0.01), scale=.7)
        
        self.ImgBtn5.bind(DirectGuiGlobals.B2PRESS, self.delete_button)
        self.ImgBtn5.bind(DirectGuiGlobals.B3PRESS, self.ImgBtn5.editStart)
        self.ImgBtn5.bind(DirectGuiGlobals.B3RELEASE, self.edit_stop)

    def delete_button(self, dispatch):
        self.button.destroy()
        
    def hide(self):
        self.button.hide()
        
    def show(self):
        self.button.show()
        
    def place(self):
        self.button.place()
        
    def set_pos(self, x, y, z):
        self.button.set_pos(x, y, z)
    
    def edit_stop(self, dispatch):
        self.ImgBtn5.editStop(dispatch)
        
moviemaker = MovieMaker()            