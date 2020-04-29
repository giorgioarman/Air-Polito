package com.ArmaniDio.airpolito;

import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import android.util.Log;
import android.view.MenuItem;
import android.os.Bundle;

import com.google.android.material.navigation.NavigationView;

import java.util.List;

public class MainActivity extends AppCompatActivity implements NavigationView.OnNavigationItemSelectedListener {


    private NavigationView navigationView;
    private final static String TAG = "MainActivity";
    private static String STATE_SELECTED_POSITION = "state_selected_position";

    //0 = Monitoring Online; 1 = location; 2 = project_detail; 3= ipqa_detail
    private int currentSelectedPosition;


    private OnlineMonitoringFragment onlineMonitoringFragment;
    private LocationFragment locationFragment;
    private ProjectFragment projectFragment;
    private IpqaFragment ipqaFragment;
    private WhoFragment whoFragment;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        setupNavigation();

        if (savedInstanceState == null)
            selectItem(0);
    }

    private void setupNavigation() {
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        navigationView = findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);
    }

    public void selectItem(int position) {

        Fragment fragment = null;

        // before creating a new fragment we should check if the already displayed one is the same we want to open
        FragmentManager fragmentManager = getSupportFragmentManager();

        List<Fragment> fragments = fragmentManager.getFragments();

        Log.d(TAG, "Fragments count: " + fragments.size());

        for (Fragment fr : fragments) {
            if ((fr instanceof OnlineMonitoringFragment) ||
                    (fr instanceof  LocationFragment) ||
                    (fr instanceof ProjectFragment)||
                    (fr instanceof IpqaFragment) ||
                    (fr instanceof WhoFragment)){
                fragment = fr;
                break;
            }
        }

        currentSelectedPosition = position;

        boolean changed = false;
        switch (position) {
            case 0:
                if (!(fragment instanceof OnlineMonitoringFragment)) {
                    onlineMonitoringFragment = new OnlineMonitoringFragment();
                    fragment = onlineMonitoringFragment;
                    changed = true;
                }

                getSupportActionBar().setTitle(R.string.online_monitoring);

                navigationView.setCheckedItem(R.id.nav_online_monitoring);
                break;

            case 1:

                if (!(fragment instanceof LocationFragment)) {
                    locationFragment = new LocationFragment();
                    fragment = locationFragment;
                    changed = true;
                }

                getSupportActionBar().setTitle(R.string.location);

                navigationView.setCheckedItem(R.id.nav_location);
                break;
            case 2:

                if (!(fragment instanceof ProjectFragment)) {
                    projectFragment = new ProjectFragment();
                    fragment = projectFragment;
                    changed = true;
                }

                getSupportActionBar().setTitle(R.string.project_detail);
                navigationView.setCheckedItem(R.id.nav_project_detail);
                break;

            case 3:

                if (!(fragment instanceof IpqaFragment)) {
                    ipqaFragment = new IpqaFragment();
                    fragment = ipqaFragment;
                    changed = true;
                }

                getSupportActionBar().setTitle(R.string.ipqa_detail);
                navigationView.setCheckedItem(R.id.nav_ipqa);
                break;
            case 4:

                if (!(fragment instanceof WhoFragment)) {
                    whoFragment = new WhoFragment();
                    fragment = whoFragment;
                    changed = true;
                }

                getSupportActionBar().setTitle(R.string.who_we_are);
                navigationView.setCheckedItem(R.id.nav_who_we_are);
                break;
            default:
                break;
        }

        if (fragment != null && changed) {
            fragmentManager.beginTransaction().replace(R.id.main_container, fragment).commit();
        } else {
            Log.d("MainActivity", "No need to change the fragment");
        }
    }


    @Override
    protected void onResume() {
        super.onResume();
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        }
        else {
            super.onBackPressed();
        }
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_online_monitoring) {
            selectItem(0);
        } else if (id == R.id.nav_location) {
            selectItem(1);
        } else if (id == R.id.nav_project_detail) {
            selectItem(2);
        }else if (id == R.id.nav_ipqa) {
            selectItem(3);
        }else if (id == R.id.nav_who_we_are) {
            selectItem(4);
        }

        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    @Override
    public void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putInt(STATE_SELECTED_POSITION, currentSelectedPosition);
    }

    @Override
    protected void onRestoreInstanceState(Bundle savedInstanceState) {
        super.onRestoreInstanceState(savedInstanceState);
        currentSelectedPosition = savedInstanceState.getInt(STATE_SELECTED_POSITION);
        selectItem(currentSelectedPosition);
    }
}
