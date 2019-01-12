class GSA_DataConfig:
    __NumberOfParticles=10 # Population Size
    __TotalTime = 1000
    __trials = 25
    __beta = 0.98
    __t0 = 1
    __Gt0 = 0.0001
    __epsilon = 8000

    @classmethod
    def get_NumberOfParticles(cls):
        return cls.__NumberOfParticles

    @classmethod
    def get_totalTime(cls):
        return cls.__TotalTime

    @classmethod
    def get_trials(cls):
        return cls.__trials

    @classmethod
    def get_beta(cls):
        return cls.__beta

    @classmethod
    def get_t0(cls):
        return cls.__t0

    @classmethod
    def get_Gt0(cls):
        return cls.__Gt0

    @classmethod
    def get_epsilon(cls):
        return cls.__epsilon