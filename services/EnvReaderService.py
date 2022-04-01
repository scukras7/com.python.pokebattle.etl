class EnvReaderService:

    def __init__(self, profile):
        self.envVars = self._readProfile(profile)

    def vars (self):
        return self.envVars

    def _readProfile(self, profile):
        rows = []
        envVars = {}
        filename = ''

        if profile == 'uat':
            filename = '../.env.uat'
        
        elif profile == 'production':
            filename = '../.env.production'

        else: # profile == 'development'
            filename = '../.env.development'
        
        passthru = [ rows.append(row.replace('\n', '')) for row in open(filename, 'r') ]
        for row in rows:
            ary = row.split('=')
            envVars[ary[0]] = ary[1]

        return envVars
