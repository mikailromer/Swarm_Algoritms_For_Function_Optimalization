class FA_DataConfig:
    __NumberOfFireflies=4 # Population Size
    __Iteration = 400
    __MaxGeneration = 1
    __Lambda=0.02
    __Beta0=1

    @classmethod
    def get_NumberOfFireflies(cls):
        return cls.__NumberOfFireflies

    @classmethod
    def get_numberOfGenerations(cls):
        return cls.__MaxGeneration

    @classmethod
    def get_Lambda(cls):
        return cls.__Lambda

    @classmethod
    def get_beta0(cls):
        return cls.__Beta0

    @classmethod
    def get_iteration(cls):
        return cls.__Iteration
