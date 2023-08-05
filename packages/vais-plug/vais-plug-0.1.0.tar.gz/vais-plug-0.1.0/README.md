# Skeleton Plugin


# Plugin skeleton V1

## Flow handle job

- Step 1: Register worker with backend (by env BACKEND_ENDPOINT) with some information (JOB_QUEUE, PLUGIN_CODE, PLUGIN_NAME, PLUGIN_DESCRIPTION, VERSION_CODE)
- Step 2: Connect to Redis, Elastic search (via env REDIS_HOST, REDIS_PORT, ELASTICSEARCH_URL)
- Step 3: Listen redis queue job (JOB_QUEUE) 
- Step 4: Handle job

Note: Using file rq_push_job.py for testing push job

## Custom an plugin

- Step 1: Inheritance class PluginSkeleton and overwrite function preload for load model if need (in sample_plugin.py).
- Step 2: Custom function handle_job() inside file sample_plugin.py (keep input parameters)


## Check list migrate skeleton plugin

- News footprint handle job function: handle_job(doc_index, doc_id, input_data=None, depended_jobs=None)
- Get input data from depended jod: input_data = SamplePlugin.get_depended_jobs_output(current_job, input_data, depended_jobs)
- Input data have new structure, so need to change the way to parse data from input data
```json
{
        "plugin_code":{
            "data": {},
            "version_code": {}
        },
        "plugin_code":{
            "data": {},
            "version_code": {}
        },
        ...
    }
```
- Change in func push result. Now doc_index come before doc_id and need to input version code: PluginSkeleton.push_result(doc_index, doc_id, output, KeywordPlugin.VERSION_CODE)
- output parameter in push_result func is just content in "data" field
- "return" in an plugin now need to using this function: plugin_skeleton.PluginSkeleton.get_output_result(output, KeywordPlugin.VERSION_CODE) 
- In docker-compose.yml file need include DEPENDED_PLUGIN_CODE envs (e.g. 'asr,speech_cluster'). It's list of depended plugin code, separate with a comma

- build lib
```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```