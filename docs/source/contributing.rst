===============
Developer Guide
===============

.. contents:: Table of Contents
   :local:

Getting Started
===============

We use Docker and Docker-Compose for managing the databases: Blazegraph and Redis, the webserver: Nginx/Flask/Conda, and Redis-Queue (RQ) workers: mostly in Conda. The official `Install Docker Compose guide`_ lists steps for installing both the base Docker Engine, and for installing Docker-Compose separately if you're on Linux. For Mac and Windows users, Docker-Compose comes bundled with Docker Engine.

You'll probably also want to `install Miniconda`_ as we bundle most dependencies in Conda environments.

.. _`Install Docker Compose guide`: https://docs.docker.com/compose/install/
.. _`install Miniconda`: https://conda.io/docs/install/quick.html

Terminology
-----------

====================  =====
Used Interchangeably  Notes
====================  =====
jobs, tasks           A job in RQ is typically called a task when discussing the front-end.
endpoint, api         We prefer to use endpoint for a route in Flask which the front-end interacts with.
spfy, this repo       The superphy/backend repo.
====================  =====

Genome Files for testing
------------------------

For testing purposes, we use E.coli genome files from GenBank. A list of ftp
links is available at the `old github/semantic repo`_. There should be 5353
genome files in total a .zip of which is available within the NML.

.. _`old github/semantic repo`: https://raw.githubusercontent.com/superphy/semantic/master/superphy/src/upload/python/data/download_files.txt

Docker Caveats
--------------

We've had problems with Ubuntu Desktop versions 16.04.2 LTS and 17.04 not connecting to NPM when building Docker images and from within the building. Builds work fine with Ubuntu Server 16.04.2 LTS on Cybera and for Ubuntu Server 12.04 or 14.04 LTS on Travis-CI. Within the building, RHEL-based operating systems (CentOS / Scientific Linux) build our NPM-dependent images (namely, `reactapp`_) just fine.

For RHEL-based OSs, I don't recommend using `devicemapper`, but instead use `overlayfs`. Reasons are documented at https://github.com/moby/moby/issues/3182. There is a guide on setting up Docker with `overlayfs` at https://dcos.io/docs/1.7/administration/installing/custom/system-requirements/install-docker-centos/, though I haven't personally tested it.

If you do end up using `devicemapper` and run into disk space issues, such as:

.. code-block:: bash

  172.18.0.1 - - [05/Jun/2017:17:50:01 +0000] "GET / HTTP/1.1" 200 12685 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36" "-"
  2017/06/05 17:50:13 [warn] 11#11: *2 a client request body is buffered to a temporary file /var/cache/nginx/client_temp/0000000001, client: 172.18.0.1, server: , request: "POST /upload HTTP/1.1", host: "localhost:8000", referrer: "http://localhost:8000/"
  [2017-06-05 17:58:31,417] ERROR in app: Exception on /upload [POST]
  Traceback (most recent call last):
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/flask/app.py", line 1982, in wsgi_app
      response = self.full_dispatch_request()
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/flask/app.py", line 1614, in full_dispatch_request
      rv = self.handle_user_exception(e)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/flask_cors/extension.py", line 161, in wrapped_function
      return cors_after_request(app.make_response(f(*args, **kwargs)))
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/flask/app.py", line 1517, in handle_user_exception
      reraise(exc_type, exc_value, tb)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/flask/app.py", line 1612, in full_dispatch_request
      rv = self.dispatch_request()
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/flask/app.py", line 1598, in dispatch_request
      return self.view_functions[rule.endpoint](**req.view_args)
    File "./routes/views.py", line 86, in upload
      form = request.form
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/local.py", line 343, in __getattr__
      return getattr(self._get_current_object(), name)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/utils.py", line 73, in __get__
      value = self.func(obj)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/wrappers.py", line 492, in form
      self._load_form_data()
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/flask/wrappers.py", line 185, in _load_form_data
      RequestBase._load_form_data(self)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/wrappers.py", line 361, in _load_form_data
      mimetype, content_length, options)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/formparser.py", line 195, in parse
      content_length, options)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/formparser.py", line 100, in wrapper
      return f(self, stream, *args, **kwargs)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/formparser.py", line 212, in _parse_multipart
      form, files = parser.parse(stream, boundary, content_length)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/formparser.py", line 523, in parse
      return self.cls(form), self.cls(files)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/datastructures.py", line 384, in __init__
      for key, value in mapping or ():
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/formparser.py", line 521, in <genexpr>
      form = (p[1] for p in formstream if p[0] == 'form')
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/formparser.py", line 497, in parse_parts
      _write(ell)
  IOError: [Errno 28] No space left on device
  [pid: 44|app: 0|req: 2/2] 172.18.0.1 () {46 vars in 867 bytes} [Mon Jun  5 17:53:08 2017] POST /upload => generated 291 bytes in 323526 msecs (HTTP/1.1 500) 2 headers in 84 bytes (54065 switches on core 0)
  172.18.0.1 - - [05/Jun/2017:17:58:32 +0000] "POST /upload HTTP/1.1" 500 291 "http://localhost:8000/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36" "-"

Which was displayed by running:

.. code-block:: bash

  docker-compose logs backend_webserver_1

You will have to increase the volume disk sizes: https://forums.docker.com/t/increase-container-volume-disk-size/1652/8

.. code-block:: bash

  # With Centos 7 I did the following to increase the default size of the containers
  # Modify the docker config in /etc/sysconfig/docker-storage to add the line:
  DOCKER_STORAGE_OPTIONS= - -storage-opt dm.basesize=20G
  service docker stop
  rm /var/lib/docker NOTE THIS DELETES ALL IMAGES etc. SO MAKE A BACKUP
  service docker start
  docker load < [each_save_in_backup.tar]
  docker run -i -t [imagename] /bin/bash
  # In the bash prompt of the docker container "df -k" should show 20GB / file system size now.

Adding a New Module
===================

There are a few ways of adding a new module:

1. Integrate your code into the Spfy codebase and update the RQ workers accordingly.
2. Add a enqueuing method to Spfy's code, but then create a new queue and a new docker image, with additional dependencies, which is added to Spfy's docker-compose.yml file.
3. Setting up your module as a microservice running in its own Docker container, add a worker to handle requests to RQ.

Currently, we only have documentation supporting option 1.

If you wish to integrate your code with Spfy, you'll have to update any dependencies to the underlying Conda-based image the RQ workers depend on. You'll also have to include your code in the `/app` directory of this repo, as that is the only directory the current RQ workers contain. The intended structure is to create a directory in `/app/modules` for your codebase and a `.py` file above at `/app/modules/newmodule.py`, for example, which contains the method your `Queue.enqueue()` function uses.

There is more specific documentation for this process in `Directly Adding a New Module`_.

If you wish to create your own image, you can use the RQ `worker`_ image as a starting point. Specifically you'll want to add your repo as a git submodule in `superphy/backend` and modify the `COPY ./app /app` to target your repo, similar to the way `reactapp`_ is included. You'll also want to take a look at the `supervisord-rq.conf`_ which controls the RQ workers. 

There is more specific documentation for this process in `Indirectly Adding a New Module`_.

In both cases, the spfy webserver will have to be modified in order for the front-end to have an endpoint target; this is documented in `Adding an Endpoint in Flask`_. The front-end will also have to be modified for there to be a form to submit tasks and have a results view generated for your new module; this is documented in `Modifying the Front-End`_.

Adding an Endpoint in Flask
---------------------------

We use `Flask Blueprints`_ to compartmentalize all routes. They are contained in `/app/routes` and have the following basic structure:

.. code-block:: python

  from flask import Blueprint, request, jsonify

  bp_someroutes = Blueprint('someroutes', __name__)

  # if methods is not defined, default only allows GET
  @bp_someroutes.route('/api/v0/someroute', methods=['POST'])
  def someroute():
    form = request.form
    return jsonify('Got your form')

Note that a blueprint can have multiple routes defined in it such as in `ra_views.py`_ which is used to build the group options for Fisher's comparison. To add a new route, create a python file such as `/app/routes/someroutes.py` with the above structure. Then in the app `factory.py`_ import your blueprint via:

.. code-block:: python

  from routes.someroute import bp_someroute

and register your blueprint in `create_app()` by adding:

.. code-block:: python
  
  app.register_blueprint(bp_someroute)

Note that we allow CORS on all routes of form `/api/*` such as `/api/v0/someroute`. This is required as the front-end `reactapp`_ is deployed in a separate container (and has a sepearate IP Address) from the Flask app.

.. _`Flask Blueprints`: http://flask.pocoo.org/docs/0.12/blueprints/
.. _`ra_views.py`: https://github.com/superphy/backend/blob/master/app/routes/ra_views.py
.. _`factory.py`: https://github.com/superphy/backend/blob/master/app/factory.py

You will then have to enqueue a job, based off that request form. There is an example of how form parsing is handled for Subtyping in the `upload()` method of `ra_posts.py`_.

If you're integrating your codebase with Spfy, add your code to a new directory in `/app/modules` and a method to enqueue in `/app/modules/somemodule.py` for example. The `gc.py`_ file resembles a basic template for a method to enqueue. 

.. code-block:: python

  import logging
  import config
  import redis
  from rq import Queue
  from modules.groupComparisons.groupcomparisons import groupcomparisons
  from modules.loggingFunctions import initialize_logging

  # logging
  log_file = initialize_logging()
  log = logging.getLogger(__name__)

  redis_url = config.REDIS_URL
  redis_conn = redis.from_url(redis_url)
  multiples_q = Queue('multiples', connection=redis_conn, default_timeout=600)

  def blob_gc_enqueue(query, target):
      job_gc = multiples_q.enqueue(groupcomparisons, query, target, result_ttl=-1)
      log.info('JOB ID IS: ' + job_gc.get_id())
      return job_gc.get_id()

Of note is that when calling RQ's enqueue() method, a custom Job class is returned. It is important that our enqueuing method returns the job id to flask, which is typically some hash such as:

.. code-block:: python

  16515ba5-040d-4315-9c88-a3bf5bfbe84e

Generally, we expect the return from Flask (to the front-end) to be a dictionary with the job id as the key to another dictionary with keys `analysis` and `file` (if relevant), though this is not strictly required (a single line containing the key will also work, as you handle naming of analysis again when doing a `dispatch()` in `reactapp`_ - more on this later). For example, a return might be:

.. code-block:: python

  "c96619b8-b089-4a3a-8dd2-b09b5d5e38e9": {
    "analysis": "Virulence Factors and Serotype",
    "file": "/datastore/2017-06-14-21-26-43-375215-GCA_001683595.1_NGF2_genomic.fna"
  }

It is expected that only 1 job id be returned per request. In `v4.2.2`_ we introduced the concept of `blob` ids in which dependency checking is handled server-side; you can find more details about this in `reactapp issue #30`_ and `backend issue #90`_. The Redis DB was also set to run in persistant-mode, with results stored to disk inside a docker volume. The `blob` concept is only relevant if you handle parallelism & pipelines for a given task (ex. Subtyping) through multiple RQ jobs (ex. QC, ID Reservation, ECTyper, RGI, parsing, etc.); if you handle parallelism in your own codebase, then this isn't required.

Another point to note is that the:

.. code-block:: python

  result_ttl=-1

parameter in the `enqueue()` method is required to store the result in Redis permanently; this is done so results will forever be available to the front-end. If we ever scale Spfy to widespread usage, it may be worth setting a ttl of 48 hours or so via:

.. code-block:: python

  result_ttl=172800

where the ttl is measured in seconds. A warning message would also have to be added to `reactapp`_.

.. _`ra_posts.py`: https://github.com/superphy/backend/blob/master/app/routes/ra_posts.py
.. _`v4.2.2`: https://github.com/superphy/backend/releases/tag/v4.2.2
.. _`reactapp issue #30`: https://github.com/superphy/reactapp/issues/30
.. _`backend issue #90`: https://github.com/superphy/backend/issues/90
.. _`gc.py`: https://github.com/superphy/backend/blob/master/app/modules/gc.py

OPTIONAL: Adding a new Queue
----------------------------

Normally, we distribute tasks between two main queues: `singles` and `multiples`. The singles queue is intended for tasks that can't be run in parallel within the same container (though you can probably run multiple containers, if you so wish); our use-case is for ECTyper. Everything else is intended to be run on the `mulitples` queue.

If you wish to add your own Queue, you'll have to create some worker to listen to it. Ideally, do this by creating a new Docker container for your worker by copying the `worker`_ Dockerfile as your starting point then copying and modifying the `supervisord-rq.conf`_ to listen to your new queue. Specifically, the:

.. code-block:: bash
  
  command=/opt/conda/envs/backend/bin/rq worker -c config multiples

would have to be modified to target the name of the new Queue your container listens to; by replacing `multiples` with `newqueue`, for example.

Eventually, we may wish to add priority queues once the number of tasks become large and we have long-running tasks alongside ones that should immediately return to the user. This can be defined by the order in which queues are named in the supervisord command:

.. code-block:: bash
  
  command=/opt/conda/envs/backend/bin/rq worker -c config multiples

For example, queues `dog` and `cat` can be ordered:

.. code-block:: bash
  
  command=/opt/conda/envs/backend/bin/rq worker -c config dog cat

which instructs the RQ workers to run tasks in `dog` first, before running tasks in `cat`.

Modifying the Front-End
-----------------------

I'd recommend you leave Spfy's setup running in Docker-Compose and run the reactapp live so you can see immediate updates.

To get started, `install node`_ and then `install yarn`_. For debugging, I also recommend using Google Chrome and installing the `React Dev Tools`_ and `Redux Dev Tools`_.

.. _`React Dev Tools`: https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi?hl=en
.. _`Redux Dev Tools`: https://chrome.google.com/webstore/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd?hl=en

Then, with Spfy's composition running, you'll want to clone `reactapp`_ and modify `ROOT` api address in `api.js`_ to point to your localhost:

.. code-block:: jsx
  
  const ROOT = 'http://localhost:8000/'

and run:

.. code-block:: bash

  cd reactapp/
  yarn install
  yarn start

Our `reactapp`_ uses `Redux` to store jobs, but also uses regular `React states` when building forms or displaying results. This was done so you don't have to be too familiar with Redux when building new modules. The codebase is largely JSX+ES6.

The first thing you'll want to do is add a description of your module to `api.js`_. For example, the old analyses const is:

.. code-block:: jsx

  export const analyses = [{
    'analysis':'subtyping',
    'description':'Serotype, Virulence Factors, Antimicrobial Resistance',
    'text':(
      <p>
        Upload genome files & determine associated subtypes.
        <br></br>
        Subtyping is powered by <a href="https://github.com/phac-nml/ecoli_serotyping">ECTyper</a>.
        AMR is powered by <a href="https://card.mcmaster.ca/analyze/rgi">CARD</a>.
      </p>
    )
  },{
    'analysis':'fishers',
    'description':"Group comparisons using Fisher's Exact Test",
    'text':'Select groups from uploaded genomes & compare for a chosen target datum.'
  }]

If we added a new module called `ml`, analyses might be:

.. code-block:: jsx

  export const analyses = [{
    'analysis':'subtyping',
    'description':'Serotype, Virulence Factors, Antimicrobial Resistance',
    'text':(
      <p>
        Upload genome files & determine associated subtypes.
        <br></br>
        Subtyping is powered by <a href="https://github.com/phac-nml/ecoli_serotyping">ECTyper</a>.
        AMR is powered by <a href="https://card.mcmaster.ca/analyze/rgi">CARD</a>.
      </p>
    )
  },{
    'analysis':'fishers',
    'description':"Group comparisons using Fisher's Exact Test",
    'text':'Select groups from uploaded genomes & compare for a chosen target datum.'
  },{
    'analysis':'ml',
    'description': "Machine learning module for Spfy",
    'text': 'Multiple machine learning algorithms such as, support vector machines, naive Bayes, and the Perceptron algorithm.'
  }]

This will create a new card for in tasks at the root page.

  A note on terminology: we consider `containers` to be *Redux-aware*; that is, they require the `connect()` function from `react-redux`. `Components` are generally not directly connected to Redux and instead get information from the Redux store passed down to it via the componenet's `props`. Note that this is not strictly true as we make use of `react-refetch`, which is a fork of Redux and uses a separate `connect()` function, to poll for job statuses and results. However, the interaction between `react-refetch` and `redux` is largely abstracted away from you and instead maps a components props directly to updates via `react-refetch` - you don't have to dispatch actions or pull down updates separately.

Then create a container in `/src/containers` which will be your request form. You can look at `Subtyping.js`_ for an example.

.. code-block:: jsx

  import React, { PureComponent } from 'react';
  // react-md
  import FileInput from 'react-md/lib/FileInputs';
  import Checkbox from 'react-md/lib/SelectionControls/Checkbox'
  import TextField from 'react-md/lib/TextFields';
  import Button from 'react-md/lib/Buttons';
  import Switch from 'react-md/lib/SelectionControls/Switch';
  import Subheader from 'react-md/lib/Subheaders';
  import CircularProgress from 'react-md/lib/Progress/CircularProgress';
  // redux
  import { connect } from 'react-redux'
  import { addJob } from '../actions'
  import { subtypingDescription } from '../middleware/subtyping'
  // axios
  import axios from 'axios'
  import { API_ROOT } from '../middleware/api'
  // router
  import { Redirect } from 'react-router'
  import Loading from '../components/Loading'

  class Subtyping extends PureComponent {
    constructor(props) {
      super(props);
      this.state = {
        file: null,
        pi: 90,
        amr: false,
        serotype: true,
        vf: true,
        submitted: false,
        open: false,
        msg: '',
        jobId: "",
        hasResult: false,
        groupresults: true,
        progress: 0
      }
    }
    _selectFile = (file) => {
      console.log(file)
      if (!file) { return; }
      this.setState({ file });
    }
    _updatePi = (value) => {
      this.setState({ pi: value });
    }
    _updateSerotype = (value) => {
      this.setState({ serotype: value })
    }
    _updateAmr = (value) => {
      this.setState({ amr: value })
    }
    _updateVf = (value) => {
      this.setState({ vf: value })
    }
    _updateGroupResults = (groupresults) => {
      this.setState({ groupresults })
    }
    _updateUploadProgress = ( progress ) => {
      this.setState({progress})
    }
    _handleSubmit = (e) => {
      e.preventDefault() // disable default HTML form behavior
      // open and msg are for Snackbar
      // uploading is to notify users
      this.setState({
        uploading: true
      });
      // configure a progress for axios
      const createConfig = (_updateUploadProgress) => {
        var config = {
          onUploadProgress: function(progressEvent) {
            var percentCompleted = Math.round( (progressEvent.loaded * 100) / progressEvent.total );
            _updateUploadProgress(percentCompleted)
          }
        }
        return config
      }
      // create form data with files
      var data = new FormData()
      // eslint-disable-next-line
      this.state.file.map((f) => {
        data.append('file', f)
      })
      // append options
      // to match spfy(angular)'s format, we dont use a dict
      data.append('options.pi', this.state.pi)
      data.append('options.amr', this.state.amr)
      data.append('options.serotype', this.state.serotype)
      data.append('options.vf', this.state.vf)
      // new option added in 4.2.0, group all files into a single result
      // this means polling in handled server-side
      data.append('options.groupresults', this.state.groupresults)
      // put
      axios.post(API_ROOT + 'upload', data, createConfig(this._updateUploadProgress))
        .then(response => {
          console.log(response)
          // no longer uploading
          this.setState({
            uploading: false
          })
          let jobs = response.data
          // handle the return
          for(let job in jobs){
            let f = (this.state.file.length > 1 ?
            String(this.state.file.length + ' Files')
            :this.state.file[0].name)
            if(jobs[job].analysis === "Antimicrobial Resistance"){
              this.props.dispatch(addJob(job,
                "Antimicrobial Resistance",
                new Date().toLocaleTimeString(),
                subtypingDescription(f, this.state.pi, false, false, this.state.amr)
              ))
            } else if (jobs[job].analysis === "Virulence Factors and Serotype") {
              let descrip = ''
              if (this.state.vf && this.state.serotype){descrip = "Virulence Factors and Serotype"}
              else if (this.state.vf && !this.state.serotype) {descrip = "Virulence Factors"}
              else if (!this.state.vf && this.state.serotype) {descrip = "Serotype"}
              this.props.dispatch(addJob(job,
                descrip,
                new Date().toLocaleTimeString(),
                subtypingDescription(f, this.state.pi, this.state.serotype, this.state.vf, false)
              ))
            } else if (jobs[job].analysis === "Subtyping") {
              // set the jobId state so we can use Loading
              const jobId = job
              this.setState({jobId})
              // dispatch
              this.props.dispatch(addJob(job,
                "Subtyping",
                new Date().toLocaleTimeString(),
                subtypingDescription(
                  f , this.state.pi, this.state.serotype, this.state.vf, this.state.amr)
              ))
            }
          }
          const hasResult = true
          this.setState({hasResult})
        })
    };
    render(){
      const { file, pi, amr, serotype, vf, groupresults, uploading, hasResult, progress } = this.state
      return (
        <div>
          {/* uploading bar */}
          {(uploading && !hasResult) ?
            <div>
              <CircularProgress key="progress" id="loading" value={progress} centered={false} />
              Uploading... {progress} %
            </div>
            : ""
          }
          {/* actual form */}
          {(!hasResult && !uploading)?
            <form className="md-text-container md-grid">
              <div className="md-cell md-cell--12">
                <FileInput
                  id="inputFile"
                  secondary
                  label="Select File(s)"
                  onChange={this._selectFile}
                  multiple
                />
                <Switch
                  id="groupResults"
                  name="groupResults"
                  label="Group files into a single result"
                  checked={groupresults}
                  onChange={this._updateGroupResults}
                />
                {!groupresults ?
                  <Subheader primaryText="(Will split files & subtyping methods into separate results)" inset />
                : ''}
                <Checkbox
                  id="serotype"
                  name="check serotype"
                  checked={serotype}
                  onChange={this._updateSerotype}
                  label="Serotype"
                />
                <Checkbox
                  id="vf"
                  name="check vf"
                  checked={vf}
                  onChange={this._updateVf}
                  label="Virulence Factors"
                />
                <Checkbox
                  id="amr"
                  name="check amr"
                  checked={amr}
                  onChange={this._updateAmr}
                  label="Antimicrobial Resistance"
                />
                {amr ?
                  <Subheader primaryText="(Note: AMR increases run-time by several minutes per file)" inset />
                : ''}
                <TextField
                  id="pi"
                  value={pi}
                  onChange={this._updatePi}
                  helpText="Percent Identity for BLAST"
                />
                <Button
                  raised
                  secondary
                  type="submit"
                  label="Submit"
                  disabled={!file}
                  onClick={this._handleSubmit}
                />
              </div>
              <div className="md-cell md-cell--12">
                {this.state.file ? this.state.file.map(f => (
                  <TextField
                    key={f.name}
                    defaultValue={f.name}
                  />
                )) : ''}
              </div>
            </form> :
            // if results are grouped, display the Loading page
            // else, results are separate and display the JobsList cards page
            (!uploading?(!groupresults?
              <Redirect to='/results' />:
              <Loading jobId={this.state.jobId} />
            ):"")
          }
        </div>
      )
    }
  }

  Subtyping = connect()(Subtyping)

  export default Subtyping


The important part to note is the form submission:

.. code-block:: jsx

  axios.post(API_ROOT + 'upload', data, createConfig(this._updateUploadProgress))
        .then(response => {
          console.log(response)
          // no longer uploading
          this.setState({
            uploading: false
          })
          let jobs = response.data
          // handle the return
          for(let job in jobs){
            let f = (this.state.file.length > 1 ?
            String(this.state.file.length + ' Files')
            :this.state.file[0].name)
            if(jobs[job].analysis === "Antimicrobial Resistance"){
              this.props.dispatch(addJob(job,
                "Antimicrobial Resistance",
                new Date().toLocaleTimeString(),
                subtypingDescription(f, this.state.pi, false, false, this.state.amr)
              ))

(truncated)

We can take a look at a simpler example in `Fishers.js`_ where there aren't multiple `jobs[job].analysis === "Antimicrobial Resistance"` analysis types in a single form.

.. code-block:: jsx

  axios.post(API_ROOT + 'newgroupcomparison', {
        groups: groups,
        target: target
      })
        .then(response => {
          console.log(response);
          const jobId = response.data;
          const hasResult = true;
          this.setState({jobId})
          this.setState({hasResult})
          // add jobid to redux store
          this.props.dispatch(addJob(jobId,
            'fishers',
            new Date().toLocaleTimeString(),
            fishersDescription(groups, target)
          ))
        });

First you'd want to change the POST route so it targets your new endpoint.

.. code-block:: jsx

  axios.post(API_ROOT + 'someroute', {

Note that `API_ROOT` prepends the `api/v0/` so the full route might be `api/v0/someroute`.

Now we need to dispatch an `addJob` action to Redux. This stores the job information in our Redux store, under the `jobs` list. In our example, we used a function to generate the description, but if you were to add a dispatch for your `ml` module you might do something like:

.. code-block:: jsx

  axios.post(API_ROOT + 'someroute', {
          groups: groups,
          target: target
        })
          .then(response => {
            console.log(response);
            const jobId = response.data;
            const hasResult = true;
            this.setState({jobId})
            this.setState({hasResult})
            // add jobid to redux store
            this.props.dispatch(addJob(jobId,
              'ml',
              new Date().toLocaleTimeString(),
              'my description of what ml options were chosen'
            ))
          });

Then, after creating your form, in `/src/containers/App.js`_ add an import for your container:

.. code-block:: jsx

  import ML from '../containers/ML'

then add a route:

.. code-block:: jsx

   <Switch key={location.key}>
      <Route exact path="/" location={location} component={Home} />
      <Route path="/fishers" location={location} component={Fishers} />
      <Route path="/subtyping" location={location} component={Subtyping} />
      <Route exact path="/results" location={location} component={Results} />
      <Route path="/results/:hash" location={location} component={VisibleResult} />
    </Switch>

would become:

.. code-block:: jsx

   <Switch key={location.key}>
      <Route exact path="/" location={location} component={Home} />
      <Route path="/fishers" location={location} component={Fishers} />
      <Route path="/subtyping" location={location} component={Subtyping} />
      <Route path="/ml" location={location} component={ML} />
      <Route exact path="/results" location={location} component={Results} />
      <Route path="/results/:hash" location={location} component={VisibleResult} />
    </Switch>

Now your form will render at `/ml`.

When your form dispatches an `addJob` action to Redux, the `/results` page will automatically populate and poll for the status of your job. You'll now need to add a component to display the results to the user. For tabular results, we use the `react-bootstrap-table`_ package. You can look at `/src/components/ResultsFishers.js`_ as a starting point.

.. _`react-bootstrap-table`: https://github.com/AllenFang/react-bootstrap-table

.. code-block:: jsx

  import React, { Component } from 'react';
  import { connect } from 'react-refetch'
  // progress bar
  import CircularProgress from 'react-md/lib/Progress/CircularProgress';
  // requests
  import { API_ROOT } from '../middleware/api'
  // Table
  import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';

  class ResultFishers extends Component {
    render() {
      const { results } = this.props
      const options = {
        searchPosition: 'left'
      };
      if (results.pending){
        return <div>Waiting for server response...<CircularProgress key="progress" id='contentLoadingProgress' /></div>
      } else if (results.rejected){
        return <div>Couldn't retrieve job: {this.props.jobId}</div>
      } else if (results.fulfilled){
        console.log(results)
        return (
          <BootstrapTable data={results.value.data} exportCSV search options={options}>
            <TableHeaderColumn  isKey dataField='0' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } width='400' csvHeader='Target'>Target</TableHeaderColumn>
            <TableHeaderColumn  dataField='1' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } csvHeader='QueryA'>QueryA</TableHeaderColumn>
            <TableHeaderColumn  dataField='2' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } csvHeader='QueryB'>QueryB</TableHeaderColumn>
            <TableHeaderColumn  dataField='3' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } width='140' csvHeader='#Present QueryA'>#Present QueryA</TableHeaderColumn>
            <TableHeaderColumn  dataField='4' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } width='140' csvHeader='#Absent QueryA'>#Absent QueryA</TableHeaderColumn>
            <TableHeaderColumn  dataField='5' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } width='140' csvHeader='#Present QueryB'>#Present QueryB</TableHeaderColumn>
            <TableHeaderColumn  dataField='6' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } width='140' csvHeader='#Absent QueryB'>#Absent QueryB</TableHeaderColumn>
            <TableHeaderColumn  dataField='7' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } width='140' csvHeader='P-Value'>P-Value</TableHeaderColumn>
            <TableHeaderColumn  dataField='8' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } width='140' csvHeader='Odds Ratio'>Odds Ratio</TableHeaderColumn>
          </BootstrapTable>
        );
      }
    }
  }

  export default connect(props => ({
    results: {url: API_ROOT + `results/${props.jobId}`}
  }))(ResultFishers)

In the case of Fisher's, the response from Flask is generated by the:

.. code-block:: python

  df.to_json(orient='split')

from the Pandas DataFrame. This creates an object with keys `columns`, `data`, and `index`. In particular, under the `data` key is an array of arrays:

.. code-block:: jsx

  [["https:\/\/www.github.com\/superphy#hlyC","O111","O24",1.0,0.0,0.0,1.0,null,1.0],["https:\/\/www.github.com\/superphy#hlyB","O111","O24",1.0,0.0,0.0,1.0,null,1.0],["https:\/\/www.github.com\/superphy#hlyA","O111","O24",1.0,0.0,0.0,1.0,null,1.0]]

(only an example, the full results.value.data array is 387 arrays long, and can vary)

Note that we use

.. code-block:: jsx

  dataField='5'

for example, which we apply to:

.. code-block:: jsx

  csvHeader='#Present QueryB'

which is used for exporting to .csv. And in between the TableHeaderColumn tags:

.. code-block:: jsx

  <TableHeaderColumn>#Present QueryB</TableHeaderColumn>

(options removed)

The `#Present QueryB` is used when displaying the webpage.

Finally, in `/src/components/ResultsTemplates.js`_ import you component:

.. code-block:: jsx

  import ResultML from './ResultML'

and add the case to the switch which decides which result view to return:

.. code-block:: javascript

  case "ml":
      return <ML jobId={job.hash} />

.. _`reactapp`: https://github.com/superphy/reactapp
.. _`supervisord-rq.conf`: https://github.com/superphy/backend/blob/master/app/supervisord-rq.conf
.. _`install node`: https://nodejs.org/en/
.. _`install yarn`: https://yarnpkg.com/en/docs/install#mac-tab
.. _`api.js`: https://github.com/superphy/reactapp/blob/master/src/middleware/api.js
.. _`Fishers.js`: https://github.com/superphy/reactapp/blob/master/src/containers/Fishers.js
.. _`Subtyping.js`: https://github.com/superphy/reactapp/blob/master/src/containers/Subtyping.js
.. _`/src/containers/App.js`: https://github.com/superphy/reactapp/blob/master/src/containers/App.js
.. _`/src/components/ResultsFishers.js`: https://github.com/superphy/reactapp/blob/master/src/components/ResultFishers.js
.. _`/src/components/ResultsTemplates.js`: https://github.com/superphy/reactapp/blob/master/src/components/ResultsTemplates.js

Directly Adding a New Module
============================

Adding Dependencies via Conda
-----------------------------

The main `environment.yml`_ file is located in our `superphy/docker-flask-conda`_
repo. This is used by the `worker`_ and `worker-blazegraph-ids`_ containers
(and the `webserver`_ container, though that may/should change). We also pull
this base superphy/docker-flask-conda image from Docker Hub. So you would have
to:

1. push the new image
2. specify the new version on each Dockerfile, namely via the

.. code-block:: bash

  FROM superphy/docker-flask-conda:2.0.0

tag.

.. _`environment.yml`: https://raw.githubusercontent.com/superphy/docker-flask-conda/master/app/environment.yml
.. _`superphy/docker-flask-conda`: https://github.com/superphy/docker-flask-conda
.. _`worker`: https://github.com/superphy/backend/blob/master/Dockerfile-rq
.. _`worker-blazegraph-ids`: https://github.com/superphy/backend/blob/master/Dockerfile-rq-blazegraph
.. _`webserver`: https://github.com/superphy/backend/blob/master/Dockerfile-spfy

Integrating your Codebase into Spfy
-----------------------------------

Indirectly Adding a New Module
==============================

Adding your Repo as a Git Submodule
-----------------------------------

Picking a Base Docker Image
---------------------------

Adding your Dependencies
------------------------

Updating Docker-Compose.yml
---------------------------
