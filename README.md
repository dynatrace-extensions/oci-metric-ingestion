## Purpose
See https://www.dynatrace.com/hub/detail/oracle-connector-hub-signals-ingest/

## Getting Started
**Note:** These actions must be done by a OCI tenancy administrator using the Oracle Cloud Shell or Oracle Code Editor.
Policies must also be configured in the OCI tenant to allow the Service Connector read metrics from the tenant. Users should do this using a group where the resource type is `serviceconnectors` before assigning the following policy: 
`Allow group <GROUP_NAME> to read metrics in tenancy`

## Setup the Application & OCI Function
1. Login to the OCI portal and navigate to **Applications** and click on 'Create Application'. 
2. Enter a name for the application and select a subnet for this application. Change the **Shape** to *GENERIC_ARM* then click on 'Create'
![alt text](images/image.png)
3. Once the application is created you will be rediected to the **Getting started** page. Launch the cloud shell and follow the instructions under **Setup fn CLI on Cloud Shell**.
![alt text](images/image-1.png)
4. In the cloud shell clone the OCI Function from this github repository and enter the directory.
![alt text](images/image-2.png)
5. Edit the `func.yaml` file using your preferred text editor (`vim` or `nano`) and set the value of `DYNATRACE_TENANT` to your Dynatrace tenant URL. If you're using new Dynatrace then the you may need to replace 'apps' with 'live' in the tenant URL.  
Ex: `https://<tenant id>.apps.dynatrace.com` should be `https://<tenant id>.live.dyntrace.com`
    - If you're using token based authentication, set the  value of  `DYNATRACE_API_KEY` to an API token that has the `metrics.ingest` scope.
    - If you're using an OAuth2 Client for authentication change the `AUTH_METHOD` to `oauth` and enter your client_id, client_secret and URN. Please see the "Configuring an OAuth2 Client" section for more details on the requirements.
![alt text](images/image-13.png)
    - Set the configuration option `IMPORT_ALL_METRICS` if you want to import metrics from a namespace that is not supported by the OCI extension. These metrics will not have metadata associated with them.
6. Save and exit the text editor. Now deploy the function using the command `fn -v deploy --app <application name>`
![alt text](images/image-3.png)
If the deployment succeeded then you should see the image in your OCI container registry.
![alt text](images/image-4.png)

## Create an OCI Connector
1. Navigate to the **Connector Hub** and click on 'Create connector'.
![alt text](images/image-5.png)
2. Enter a name for the connector and select 'Monitoring' as the **Source** and 'Functions' as the **Target**
![alt text](images/image-6.png)
3. Select the compartments and namespaces you want to pull metrics from.
![alt text](images/image-7.png)
4. Scroll past **Configure task** and choose the compartment, application and function that you just created in the previous setps.
![alt text](images/image-8.png)
5. If you see a warning asking if you want to create a policy in a given compartment, you *must* click **Create**
![alt text](images/image-14.png)
6. Finally click 'Create'
![alt text](images/image-15.png)
7. Verify the metrics are getting ingested into Dynatrace.
![alt text](images/image-9.png)

## Configuring an OAuth2 Client
Using an OAuth2 client for the OCI functions will require you to add some additional policies to give the oauth token access to ingest metrics.

1. Visit your Dynatrace tenant's **Account Management** portal and navigate to **Identity & access management** -> **Policy Management**. Click on the add policy button.
![alt text](images/oauth/image.png)
2. Give the policy a name like **Metric Ingest** and paste the following policy statement into the large text box `ALLOW storage:metrics:write;` and click on **Save**
![alt text](images/oauth/image-1.png)
3. Now navigate to the **Service Users** page under **Identity & access management** and click on **Add service user**
![alt text](images/oauth/image-2.png)
4. Give the user a name and optionally a description then click on **Save**
![alt text](images/oauth/image-3.png)
5. Click on the 3 vertical dots on the right side of the page and select **View Service User**
![alt text](images/oauth/image-4.png)
6. Copy the **Service user email** that is displayed on this page, you will need it for step 9.
7. Click on the **+Permission** button and from the dropdown menu select the policy we created in step 2.
![alt text](images/oauth/image-5.png)
8. Under **Identity & access management** navigate to **OAuth clients** and click on **Create Client**
![alt text](images/oauth/image-6.png)
9. Paste the service user email address that you copied in setp 6 in the **Subject user email** text box then assign the user **Write metrics** (`storage:metrics:write`) permission.
![alt text](images/oauth/image-7.png)
![alt text](images/oauth/image-8.png)
10. Finally click on **Create Client** at the bottom of the page and copy the `client_id`, `client_secret` and `urn` for use with the OCI function.  

## Debugging 
If you are running into issues getting the connector to work, go to the application and enable **Function Invocation Logs**.
![alt text](images/image-12.png)
Any errors will be logged here as well as some information about when the function has been run.
![alt text](images/image-11.png)
