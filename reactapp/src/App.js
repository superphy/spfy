import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import NavigationDrawer from 'react-md/lib/NavigationDrawers';
import NavLink from './NavLink';

import Home from './Home';
import Page1 from './Page1';
import Page2 from './Page2';
import Page3 from './Page3';
import NewComparison from './NewComparison';

const navItems = [{
  exact: true,
  label: 'Home',
  to: '/',
  icon: 'home',
}, {
  label: 'Page 1',
  to: '/page-1',
  icon: 'bookmark',
}, {
  label: 'Page 2',
  to: '/page-2',
  icon: 'donut_large',
}, {
  label: 'Page 3',
  to: '/page-3',
  icon: 'flight_land',
}];

class App extends Component {
  render() {
    return (
      <Route
        render={({ location }) => (
          <NavigationDrawer
            drawerTitle="spfy"
            toolbarTitle="Group Comparisons"
            navItems={navItems.map(props => <NavLink {...props} key={props.to} />)}
          >
            <Switch key={location.key}>
              <Route exact path="/" location={location} component={Home} />
              <Route path="/new" location={location} component={NewComparison} />
              <Route path="/page-1" location={location} component={Page1} />
              <Route path="/page-2" location={location} component={Page2} />
              <Route path="/page-3" location={location} component={Page3} />
            </Switch>
          </NavigationDrawer>
        )}
      />
    );
  }
}

export default App;
