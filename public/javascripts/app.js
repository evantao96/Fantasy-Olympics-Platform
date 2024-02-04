Vue.component('select2', {
    props: ['options', 'value'],
    template: '#select2-template',
    mounted: function() {
        var vm = this
        $(this.$el)
            .val(this.value)
            // init select2
            .select2({ data: this.options })
            // emit event on change.
            .on('change', function() {
                var value = $(this).val();
                vm.$emit('input', JSON.stringify(value))
            })
    },
    watch: {
        value: function(value) {
            // update value
            $(this.$el).select2('val', value)
        },
        options: function(options) {
            // update options
            $(this.$el).select2({ data: options })
        }
    },
    destroyed: function() {
        $(this.$el).off().select2('destroy')
    }
})

var vm = new Vue({
    el: '#app',
    data: {
        header: '',
        location: undefined,
        date: undefined,
        weather: undefined,
        currStage: 0,
        prevStage: 0,
        name: '',
        teamName: '',
        passwd: '',
        lname: '',
        lteamName: '',
        lpasswd: '',
        isOld: false,
        stage15: false,
        stage2: false,
        events: [],
        chosenEvents: [],
        categories: {},
        chosenAthletes: [],
        public: true,
        scores: [],
        players: [],
        finished: false,
        topScores: [],
        error: false,
        error_message: ''
    },
    methods: {
        init: function() {
            var vm = this;
            vm.currStage = 1;
            vm.header = "Create or Login Player"
            vm.stage1 = true;
        },
        submitName: function() {
            if (this.name === "" || this.teamName === "") {
                this.error = true;
                this.error_message = "Please enter all fields";
                return;
            }

            this.error = false;

            var vm = this;

            axios.post('/players', {
                    name: vm.name,
                    teamName: vm.teamName,
                    passwd: vm.passwd
                })
                .then(function(response) {
                    console.log(response.data);
                    if (response.data.success) {
                        vm.currStage = 0;
                        vm.getEvents();
                        vm.header = "Loading";
                    } else if (response.data.duplicate) {
                        vm.error = true;
                        vm.error_message = "Name and team name taken";
                    } else {
                        vm.error = true;
                        vm.error_message = "Player creation failed";
                    }

                })
                .catch(function(error) {
                    console.log(error);
                });
        },
        lsubmitName: function() {
            if (this.lname === "") {
                this.error = true;
                this.error_message = "Please enter name field";
                return;
            }

            this.error = false;

            var vm = this;

            axios.post('/players/login', {
                    lname: vm.lname,
                    lteamName: vm.lteamName,
                    lpasswd: vm.lpasswd
                })
                .then(function(response) {
                    console.log(response.data);
                    vm.isOld = true;
                    if (response.data.success) {
                        vm.currStage = 0;
                        vm.getEvents();
                        vm.header = "Loading";
                    } else {
                        vm.error = true;
                        vm.error_message = "Player verification failed"
                    }

                })
                .catch(function(error) {
                    console.log(error);
                });
        },
        getWeather: function() {
            var vm = this;

            axios.get('/athletes/weather').then(function(response) {
                console.log(response.data);
                if (response.data.success) {
                    vm.location = response.data.location;
                    vm.date = response.data.date;
                    vm.weather = response.data.weather;
                } else {
                    vm.error = true;
                    vm.error_message = "Could not get weather"
                }
            });
        },
        getEvents: function() {
            var vm = this;

            vm.getWeather();

            axios.get('/events')
                .then(function(response) {
                    console.log("Done getEvents");
                    console.log(response.data);
                    if (response.data.success) {
                        vm.events = response.data.events.map(function(el) {
                            return { id: el.id, text: el.name };
                        });
                        vm.header = "Choose The Event";
                        vm.currStage = 2;
                    } else {
                        vm.error = true;
                        vm.error_message = "Could not get Events";
                    }
                })
                .catch(function(error) {
                    console.log(error);
                });
        },
        onEventChange: function(value) {
            var vm = this;

            vm.chosenEvents = JSON.parse(value)
        },
        getAthletes: function() {
            var vm = this;
            vm.chosenAthletes = [];
            axios.post('/athletes', {
                    chosenEvents: JSON.stringify(this.chosenEvents)
                })
                .then(function(response) {
                    console.log(response.data);
                    if (response.data.success) {
                        vm.categories = {};
                        for (var i in response.data.payload) {
                            let event = response.data.payload[i];
                            vm.$set(vm.categories, event.eventId, { eventName: event.eventName, athletes: event.athletes });
                        }
                        vm.header = "Choose Athletes"
                    } else {
                        vm.error = true;
                        vm.error_message = "Could not get Athletes";
                    }
                })
                .catch(function(error) {
                    console.log(error);
                });

        },
        getScores: function() {
            var vm = this;

            vm.error = false;

            vm.currStage = 0;
            vm.header = "Loading";

            if (vm.isOld) {
                vm.name = vm.lname;
                vm.teamName = vm.lteamName;
            }
            if (this.chosenAthletes.length > 10) {
                vm.error = true;
                vm.error_message = "Can only choose 10 athletes";
                return;
            }
            axios.post('/athletes/scores', {
                    chosenAthletes: JSON.stringify(this.chosenAthletes),
                    name: vm.name,
                    teamName: vm.teamName,
                    public: vm.public
                })
                .then(function(response) {
                    console.log(response.data);
                    if (response.data.success) {
                        vm.scores = response.data.scores;
                        vm.header = "Scores";
                        vm.currStage = 3;
                        window.setTimeout(vm.showScores, 750);
                    } else {
                        vm.error = true;
                        if (response.data.athlete) {
                            vm.currStage = 2;
                            vm.header = "Choose Athletes";
                            vm.chosenAthletes = [];
                            vm.getAthletes();
                            vm.error_message = response.data.athlete + " is taken by another player";
                        } else {
                            vm.error_message = "Could not get Scores";
                        }
                    }
                })
                .catch(function(error) {
                    console.log(error);
                });
        },
        playAgain: function() {
            var vm = this;

            axios.get('/players/scores/clear').then(function(response) {
                console.log(response.data);
                if (response.data.success) {
                    vm.header = "Choose Event"
                    vm.currStage = 2;
                    vm.chosenEvents = [];
                    vm.categories = {};
                    vm.chosenAthletes = [];
                    vm.players = [];
                    vm.finished = false;
                    vm.getWeather();
                } else {
                    vm.error = true;
                    vm.error_message = "Could not reset scores";
                }
            });
        },
        tweetScore: function() {
            var vm = this;
            var score = 0;
            for (var i = 0; i < vm.scores.length; i++) {
                score += vm.scores[i].points;
            }
            var tweet = "http://twitter.com/home?status=I scored " + score + " points on Fantasy Olympics!";
            window.open(tweet, '_blank');
        },
        showScores: function() {
            var vm = this;

            axios.get('/players/scores').then(function(response) {
                console.log(response.data);
                if (response.data.success) {
                    vm.players = response.data.players;
                    vm.finished = true; 
                } else {
                    vm.error = true;
                    vm.error_message = "Error retrieving scores";
                }
            });
        },
        showTopScores: function() {
            var vm = this;

            vm.prevStage = vm.currStage;
            vm.currStage = 4;

            axios.get('/players/scores/top').then(function(response) {
                console.log(response.data);
                if (response.data.success) {
                    vm.topScores = response.data.topScores;
                } else {
                    vm.error = true;
                    vm.error_message = "Error retrieving high scores";
                }
            });
        },
        goBack: function() {
            var vm = this;

            vm.currStage = vm.prevStage;
            vm.prevStage = 0;
        }
    }
});
vm.init();
