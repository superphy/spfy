import React, { PureComponent } from 'react';
import Dialog from 'react-md/lib/Dialogs';
import Button from 'react-md/lib/Buttons/Button';
import Divider from 'react-md/lib/Dividers';
import TextField from 'react-md/lib/TextFields';
import Paper from 'react-md/lib/Papers';

export default class Home extends PureComponent {
  constructor(props) {
    super(props);

    this.state = { visible: false };
  }

  openDialog = () => {
    this.setState({ visible: true });
  };

  closeDialog = () => {
    this.setState({ visible: false });
  };

  render() {
    const { visible } = this.state;
    return (
      <div className="md-grid">
        <div className="paper-container">
          <Paper>
            <div>
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean rutrum mattis lacus non pharetra. Suspendisse finibus vitae lectus ac sodales. Pellentesque et tortor eros. Nunc vitae est eget tortor condimentum ultrices. Donec a magna sed ex vulputate bibendum sit amet sit amet arcu. Curabitur blandit scelerisque augue in blandit. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nulla a dolor quis elit ullamcorper sodales eget eu lacus. Morbi velit nibh, fringilla id convallis eget, faucibus ut nisi. Nunc viverra quis tortor ac aliquet. Vestibulum vitae tempor arcu, eget tempus arcu.
              </p>
              <p>
                Etiam a augue tristique, molestie arcu ut, pulvinar metus. Sed ornare quam quis enim bibendum suscipit. Aenean metus ipsum, mattis in ultricies quis, tincidunt ut nunc. Nunc velit elit, imperdiet vitae dui non, porta tristique velit. Donec mattis scelerisque diam, a placerat massa varius at. Nunc neque sapien, congue vel pellentesque in, suscipit nec lectus. Quisque interdum tellus mauris, eget auctor nunc pulvinar vel. Cras faucibus augue ac diam dictum cursus. Cras vestibulum neque justo, sed tincidunt massa cursus vel. Nulla vel tincidunt lectus.
              </p>
            </div>
          </Paper>
          <div>
            <Button raised label="New Comparison" onClick={this.openDialog} />
            <Dialog
              id="newComparison"
              visible={visible}
              onHide={this.closeDialog}
              title="Submit a new Group Comparison"
              aria-label="New Comparison"
              modal
              actions={[{
                onClick: this.closeDialog,
                primary: true,
                label: 'Submit',
              }, {
                onClick: this.closeDialog,
                primary: true,
                label: 'Cancel',
              }]}
            >
              <form className="md-toolbar-relative">
                <TextField
                  id="eventEmail"
                  placeholder="Email"
                  defaultValue="heyfromjonathan@gmail.com"
                  block
                  paddedBlock
                />
                <Divider />
                <TextField
                  id="eventName"
                  placeholder="Event name"
                  block
                  paddedBlock
                />
                <Divider />
                <TextField
                  id="eventDescription"
                  placeholder="Description"
                  block
                  paddedBlock
                  rows={4}
                  defaultValue="asdlafkjewflaksejflakjskl"
                />
              </form>
            </Dialog>
          </div>
        </div>
      </div>
    );
  }
}
